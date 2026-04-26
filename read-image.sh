# Set the image filename here  
IMAGE="scnfmixr-v4.8.0.img.zst"

# 0) Identify and sanity-check
lsblk -f /dev/mmcblk0
mount | grep mmcblk0 || true

# 1) Make sure nothing on eMMC is mounted
sudo umount /dev/mmcblk0p1 /dev/mmcblk0p2 2>/dev/null || true

# 2) Create a truncated + compressed image (MBR/dos; p2 ends at sector 13978600)
#    We copy sectors 0..13978600 inclusive => count=13978601
sudo dd if=/dev/mmcblk0 bs=512 count=13978601 status=progress | zstd -19 -T0 -o "${IMAGE}"

# 3) Verify the compressed image
zstd -t "${IMAGE}"

# 4) (Optional) Write a checksum file
sha256sum "${IMAGE}" > "${IMAGE}.sha256"
