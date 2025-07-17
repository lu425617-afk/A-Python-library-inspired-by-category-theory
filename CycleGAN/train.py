
import time
from tqdm import tqdm  
from options.train_options import TrainOptions
from data import create_dataset
from models import create_model
from util.visualizer import Visualizer

if __name__ == '__main__':
    opt = TrainOptions().parse()  
    dataset = create_dataset(opt)  
    dataset_size = len(dataset)  
    print('The number of training images = %d' % dataset_size)

    model = create_model(opt)  
    model.setup(opt)  
    visualizer = Visualizer(opt)  
    total_iters = 0  

    for epoch in range(opt.epoch_count, opt.n_epochs + opt.n_epochs_decay + 1):
        epoch_start_time = time.time()  
        iter_data_time = time.time()  
        epoch_iter = 0  
        visualizer.reset()  
        model.update_learning_rate()  

        print(f'🚀 Training Epoch {epoch}/{opt.n_epochs + opt.n_epochs_decay}')
        
        
        with tqdm(total=dataset_size, desc=f"Epoch {epoch}") as pbar:
            for i, data in enumerate(dataset):
                iter_start_time = time.time()  
                
                if total_iters % opt.print_freq == 0:
                    t_data = iter_start_time - iter_data_time

                total_iters += opt.batch_size
                epoch_iter += opt.batch_size
                model.set_input(data)  
                model.optimize_parameters()  

                
                losses = model.get_current_losses()
                if 'G' not in losses:
                    print("⚠️ Warning: 'G' loss not found in losses dictionary. Debugging...")
                    print("losses dictionary:", losses)

                t_comp = (time.time() - iter_start_time) / opt.batch_size

                
                pbar.set_postfix({
                    'Loss_G': losses.get('G', 0.0),
                    'Loss_D_A': losses.get('D_A', 0.0),
                    'Loss_D_B': losses.get('D_B', 0.0),
                    'Time/iter (s)': f"{t_comp:.4f}"
                })
                pbar.update(1)

                
                if total_iters % opt.display_freq == 0:
                    save_result = total_iters % opt.update_html_freq == 0
                    model.compute_visuals()
                    visualizer.display_current_results(model.get_current_visuals(), epoch, save_result)

                
                if total_iters % opt.print_freq == 0:
                    visualizer.print_current_losses(epoch, epoch_iter, losses, t_comp, t_data)
                    if opt.display_id > 0:
                        visualizer.plot_current_losses(epoch, float(epoch_iter) / dataset_size, losses)

                
                if total_iters % opt.save_latest_freq == 0:
                    print(f'📌 Saving latest model at epoch {epoch}, total_iters {total_iters}')
                    save_suffix = 'iter_%d' % total_iters if opt.save_by_iter else 'latest'
                    model.save_networks(save_suffix)

                iter_data_time = time.time()

        
        if epoch % opt.save_epoch_freq == 0:
            print(f'📌 Saving model at the end of epoch {epoch}, total_iters {total_iters}')
            model.save_networks('latest')
            model.save_networks(epoch)

        print(f'✅ End of epoch {epoch} | Time: {time.time() - epoch_start_time:.2f} sec')
