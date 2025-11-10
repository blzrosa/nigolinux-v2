# nigolinux-v2
Second version of my dotfiles and archlinux basic setup installer
- Dell G15 5530 RTX 4050

# Instalation

## 1. Connecting to the internet
> [!TIP]
> If you already know the name of the connection, you can skip the first steps after `iwctl`.

```bash
iwctl

# List your devices (e.g., wlan0)
[iwctl]# device list

# Scan for networks
[iwctl]# station wlan0 scan

# List available networks
[iwctl]# station wlan0 get-networks

# Connect to your network
[iwctl]# station wlan0 connect YOUR_NETWORK_NAME
# (Type your password when prompted)

# Exit the tool
[iwctl]# exit

# Test the connection
ping -c 1 google.com
```

## 2. Updating Keyring and Archinstall

```bash
# Sync package lists
pacman -Sy

# Update the Arch keyring to avoid signature errors
pacman -S archlinux-keyring

# Install the guided installer
pacman -S archinstall
```

## 3. Disk Partitioning

> [!NOTE]
> We will partition the disk manually, then instruct archinstall to use our existing mount points. This provides more control than archinstall's default partitioning.

```bash
# List block devices to identify your drive (e.g., /dev/nvme0n1)
lsblk

# Use cfdisk to partition the target drive
cfdisk /dev/nvme0n1
```

Create the following partition layout:

1. EFI System: 1G (Type: EFI System)

2. Linux Root: XG (Remaining space, Type: Linux filesystem)

### Format and Mount Partitions
> [!CAUTION]
> Replace partition names below with your actual device names.

```bash
# List devices again to confirm partition names (e.g., nvme0n1p1, nvme0n1p2)
lsblk

# Format the EFI partition as FAT32
mkfs.fat -F32 /dev/nvme0n1p1

# Format the root partition as ext4
mkfs.ext4 /dev/nvme0n1p2

# Mount the root partition to /mnt
mount /dev/nvme0n1p2 /mnt

# Create the boot directory
mkdir /mnt/boot

# Mount the EFI partition to /mnt/boot
mount /dev/nvme0n1p1 /mnt/boot
```

## 4. Running Archinstall

With the disks mounted, run the `archinstall` script.

```bash
archinstall
```

Configure the installer with the following key settings:

> [\!IMPORTANT]
> **This is the most critical step.**
>
>   * When prompted for **"disk\_layouts" / "Disk configuration"**:
>     1.  Select your drive (e.g., `/dev/nvme0n1`).
>     2.  Choose the option **"manual partitioning"**.
>     3.  Set the mountpoint to `/mnt`

Set the rest of the options as follows:

  * **Bootloader:** `grub`
  * **Profile:** `Desktop / Hyprland`
  * **Display Manager:** `sddm`
  * **Graphics:** `Nvidia open`
  * **Audio:** `pipewire`
  * **Network:** `NetworkManager`
  * **Timezone:** `America/Sao_Paulo`
  * **Additional Packages:** `git`, `curl`, `wget`, `fastfetch`

> [!NOTE]
> The timezone here is for my setup, feel free to change it

After confirming, `archinstall` will install the system. When it finishes, **select `chroot`** to enter the new system for configuration.

## 5. Post-Installation Configuration (Inside chroot)

You are now inside your new installation. Let's configure the NVIDIA drivers and GRUB.

### NVIDIA Driver Setup

1.  **Install `nvidia-prime` and `nvidia-settings`:**

    ```bash
    pacman -S nvidia-prime nvidia-settings
    ```

2.  **Configure GRUB Kernel Parameters:**
    Edit the GRUB config file:

    ```bash
    nano /etc/default/grub
    ```

    Find the `GRUB_CMDLINE_LINUX_DEFAULT` line and add the NVIDIA parameters:

    ```conf
    # Example:
    GRUB_CMDLINE_LINUX_DEFAULT="quiet loglevel=3 nvidia_drm.modeset=1 nvme_core.default_ps_max_latency_us=0 nvidia.NVreg_DynamicPowerManagement=0 i915.enable_psr=0"
    ```

3.  **Force SDDM to use X11:**
    This is often required for NVIDIA drivers to work correctly with a display manager, even when launching a Wayland session.

    ```bash
    mkdir /etc/sddm.conf.d
    nano /etc/sddm.conf.d/10-graphics.conf
    ```

    Add the following content:

    ```ini
    [DisplayServer]
    ServerType=X11
    ```

4.  **Configure NVIDIA Kernel Modules:**
    Ensure modules load early at boot.

    ```bash
    nano /etc/modules-load.d/nvidia.conf
    ```

    Add the following:

    ```
    nvidia
    nvidia_drm
    nvidia_modeset
    ```

### Build Configs and Enable Services

1.  **Apply all configuration changes:**

    ```bash
    # Re-generate the GRUB config
    grub-mkconfig -o /boot/grub/grub.cfg

    # Re-generate the initramfs
    mkinitcpio -P
    ```

2.  **Enable NVIDIA suspend services and disable power management services:**

    ```bash
    systemctl enable nvidia-suspend.service
    systemctl enable nvidia-resume.service
    systemctl enable nvidia-hibernate.service

    # Disable conflicting power daemons
    systemctl disable nvidia-powerd.service
    systemctl disable power-profiles-daemon.service
    ```

> [!NOTE]
> This was the only way I could let the laptop close the lid and return from the suspended mode.

### Reboot

The chroot configuration is complete.

```bash
exit
reboot
```


## 6. First Boot Setup

After rebooting, log in to your new Hyprland session.

1.  **Connect to the Internet:**
    Open a terminal and use the text-based UI for NetworkManager.

    ```bash
    nmtui
    ```

    Activate your connection.

2.  **Set up SSH for GitHub:**

    ```bash
    ssh-keygen -t ed25519 -C "your.email@domain.com"
    ```

      * Press Enter to accept the default file location.
      * Enter a secure password for your key.

    Display your new public key to copy it:

    ```bash
    cat .ssh/id_ed25519.pub
    ```

> [!TIP]
> Copy the entire output (from `ssh-ed25519...` to `...domain.com`) and add it to your GitHub account under **Settings \> SSH and GPG keys \> New SSH key**.

3.  **Run Post-Install Script:**
    This will clone the `nigolinux-v2` repository, install Python, and run the main setup script.

    ```bash
    # Create a temporary directory
    mkdir temp
    cd temp

    # Clone the dotfiles/setup repository
    git clone https://github.com/blzrosa/nigolinux-v2.git

    # Enter the directory
    cd nigolinux-v2

    # Install Python
    sudo pacman -S python

    # Run the main setup script
    sudo python -m main
    ```

    Follow the instructions from the script.

4.  **Clean up:**

    ```bash
    cd ../..
    rm -rf temp
    ```

-----

## 7. Running Apps with NVIDIA GPU

Your system is now set up. To run an application using the dedicated NVIDIA GPU, use the `prime-run` command.

```bash
prime-run <program_name>

# Example:
prime-run steam
```
