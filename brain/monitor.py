import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

class TrainingMonitor:
    def __init__(self, log_dir="data/logs"):
        self.logger = logging.getLogger(__name__)
        self.log_dir = Path(log_dir)
        
        try:
            self.log_dir.mkdir(exist_ok=True, parents=True)
            self.reset_logs()
            self.logger.info("Training monitor initialized")
        except Exception as e:
            self.logger.critical(f"Failed to initialize monitor: {str(e)}")
            raise

    def log_epoch(self, epoch, train_loss, val_metrics=None):
        try:
            self.current_log["epochs"].append(epoch)
            self.current_log["train_loss"].append(train_loss)
            
            if val_metrics:
                for metric, value in val_metrics.items():
                    if metric in self.current_log["metrics"]:
                        self.current_log["metrics"][metric].append(value)
            
            self._save_log()
            self._plot_progress()
            self.logger.debug(f"Logged epoch {epoch} data")
            
        except Exception as e:
            self.logger.error(f"Failed to log epoch {epoch}: {str(e)}", exc_info=True)
            raise
    
    def _save_log(self):
        with open(self.log_dir / "training_log.json", "w") as f:
            json.dump(self.current_log, f, indent=2)
    
    def _plot_progress(self):
        plt.figure(figsize=(12, 6))
        
        # График потерь
        plt.subplot(1, 2, 1)
        plt.plot(self.current_log["epochs"], self.current_log["train_loss"], label="Train")
        if self.current_log["val_loss"]:
            plt.plot(self.current_log["epochs"], self.current_log["val_loss"], label="Val")
        plt.title("Training Loss")
        plt.xlabel("Epoch")
        plt.legend()
        plt.grid()
        
        # График метрик
        plt.subplot(1, 2, 2)
        for metric, values in self.current_log["metrics"].items():
            if values:
                plt.plot(self.current_log["epochs"], values, label=metric)
        plt.title("Validation Metrics")
        plt.xlabel("Epoch")
        plt.legend()
        plt.grid()
        
        plt.tight_layout()
        plt.savefig(self.log_dir / "training_progress.png")
        plt.close()
    
    def get_best_epoch(self, metric="accuracy"):
        if not self.current_log["metrics"].get(metric):
            return -1
        return int(np.argmax(self.current_log["metrics"][metric])) + 1
