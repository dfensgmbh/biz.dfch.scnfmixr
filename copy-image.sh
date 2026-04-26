IMAGE="scnfmixr-v4.8.0.img.zst"
TARGET="scnfmixr.img.zst"

# Create a temporary mount point
sudo mkdir -p /mnt/usb_restore

# Mount the second partition of the USB stick
sudo mount /dev/sda2 /mnt/usb_restore

# Copy the image and the checksum file to the USB stick's home directory
sudo rsync -ah --progress "${IMAGE}" "${IMAGE}.sha256" /mnt/usb_restore/home/admin/

cd /mnt/usb_restore/home/admin/
sha256sum -c "${IMAGE}.sha256"
mv "${IMAGE}" "${TARGET}"

cd ~
sudo umount /mnt/usb_restore
