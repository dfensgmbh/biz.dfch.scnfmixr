# Set the image filename here  
IMAGE="scnfmixr-v4.7.0.img.zst"

# PRE) Verify checksum before writing (must match the .sha256 file from the source)
sha256sum -c "${IMAGE}.sha256"

# 0) Identify and sanity-check you are targeting the RIGHT device
lsblk -f /dev/mmcblk0
mount | grep mmcblk0 || true

# 1) Make sure nothing on eMMC is mounted
sudo umount /dev/mmcblk0p1 /dev/mmcblk0p2 2>/dev/null || true

# 2) Restore (DESTRUCTIVE: overwrites /dev/mmcblk0)
zstd -d -c "${IMAGE}" | sudo dd of=/dev/mmcblk0 bs=4M status=progress conv=fsync
sudo sync

# 3) Ask kernel to re-read partition table (if this errors "busy", reboot and continue)
sudo partprobe /dev/mmcblk0 || true
