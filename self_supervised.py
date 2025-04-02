import torch
import torch.nn as nn
import torch.optim as optim
from utils import mask_generator, pretext_generator
from config import *
from memory_logger import *
import torch.nn.init as init

class Encoder(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(Encoder, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)
        self.sigmoid = nn.LeakyReLU(negative_slope=0.2)
    def forward(self, x):
        x = self.sigmoid(self.fc1(x))
        x = self.fc2(x)
        return x

class SelfSupervised(nn.Module):
    def __init__(self, dim, encoder, mask_estimator, feature_estimator):
        super(SelfSupervised, self).__init__()
        if(encoder == None):
            # self.encoder = Encoder(dim, 64, 32)
            self.encoder = nn.Linear(dim, 32)
            self.mask_estimator = nn.Linear(int(32), dim)
            self.feature_estimator = nn.Linear(int(32), dim)
        else:
            self.encoder = encoder
            self.mask_estimator = mask_estimator
            self.feature_estimator = feature_estimator
        
    def forward(self, x):
        hidden = torch.relu(self.encoder(x))
        mask_output = torch.sigmoid(self.mask_estimator(hidden))
        feature_output = torch.sigmoid(self.feature_estimator(hidden))
        return mask_output, feature_output

def self_supervised(encoder, mask_estimator, feature_estimator, x_unlab, p_m, alpha, console, pid, process):
    _, dim = x_unlab.shape
    device = torch.device('cuda:7' if torch.cuda.is_available() else 'cpu')
    model = SelfSupervised(dim, encoder, mask_estimator, feature_estimator).to(device)
    model.train()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.OneCycleLR(optimizer, max_lr=0.1, steps_per_epoch=len(x_unlab), epochs=5)

    criterion_mask = nn.BCELoss()
    criterion_feature = nn.MSELoss()
    m_unlab = mask_generator(p_m, x_unlab)
    m_label, x_tilde = pretext_generator(m_unlab, x_unlab)
    x_tilde = x_tilde.float().to(device)
    m_label = m_label.float().to(device)
    x_unlab = x_unlab.float().to(device)
    for epoch in range(1, EPOCHS+1):
        for i in range(0, len(x_unlab), BATCH_SIZE):
            inputs = x_tilde[i:i+BATCH_SIZE]
            labels_mask = m_label[i:i+BATCH_SIZE]
            labels_feature = x_unlab[i:i+BATCH_SIZE]
            outputs_mask, outputs_feature = model(inputs)
            loss_mask = criterion_mask(outputs_mask, labels_mask)
            loss_feature = criterion_feature(outputs_feature, labels_feature)
            loss = loss_mask + alpha * loss_feature
            # loss = loss_feature
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            torch.cuda.empty_cache()
        if(epoch%10==0):
            console.print(f"[bold white]                Epoch {epoch} : {loss.item()}[/bold white]")
        scheduler.step()
    model = model.to('cpu')
    if(process == 'ini_global_encoder'):
        from calflops import calculate_flops
        batch_size = 1
        input_shape = (batch_size, 42)
        flops, macs, params = calculate_flops(model=model, 
                                            input_shape=input_shape,
                                            output_as_string=True,
                                            output_precision=4)
        print("FLOPs:%s   MACs:%s   Params:%s \n" %(flops, macs, params))

    encoder = model.encoder
    mask_estimator = model.mask_estimator
    feature_estimator = model.feature_estimator
    return encoder, mask_estimator, feature_estimator