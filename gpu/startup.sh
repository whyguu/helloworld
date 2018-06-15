sudo systemctl stop lightdm.service
nvidia-settings -a "[gpu:0]/GPUFanControlState=1" -a "[fan:0]/GPUTargetFanSpeed=99"
nvidia-settings -a "[gpu:1]/GPUFanControlState=1" -a "[fan:1]/GPUTargetFanSpeed=99"
nvidia-settings -a "[gpu:2]/GPUFanControlState=1" -a "[fan:2]/GPUTargetFanSpeed=99"
nvidia-settings -a "[gpu:3]/GPUFanControlState=1" -a "[fan:3]/GPUTargetFanSpeed=99"

sleep 10
gnome-screensaver-command -l  
nvidia-settings -a [gpu:0]/GPUMemoryTransferRateOffset[3]=600
nvidia-settings -a [gpu:1]/GPUMemoryTransferRateOffset[3]=600
nvidia-settings -a [gpu:2]/GPUMemoryTransferRateOffset[3]=600
nvidia-settings -a [gpu:3]/GPUMemoryTransferRateOffset[3]=600
nvidia-settings -a "[gpu:0]/GPUGraphicsClockOffset[3]=60"
nvidia-settings -a "[gpu:1]/GPUGraphicsClockOffset[3]=60"
nvidia-settings -a "[gpu:2]/GPUGraphicsClockOffset[3]=60"
nvidia-settings -a "[gpu:3]/GPUGraphicsClockOffset[3]=60"
