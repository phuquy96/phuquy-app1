Add-Type -AssemblyName System.Drawing

$src = "C:\Users\Admin\.gemini\antigravity-ide\scratch\TEST_PHUQUY\logo.png"
$img = [System.Drawing.Image]::FromFile($src)
Write-Host "Logo loaded: $($img.Width)x$($img.Height)"

$destDir = "C:\Users\Admin\.gemini\antigravity-ide\scratch\TEST_PHUQUY\TEST_PHUQUY\Assets.xcassets\AppIcon.appiconset"
New-Item -ItemType Directory -Force -Path $destDir | Out-Null

$sizes = @(
    @{ name = "icon_1024.png"; size = 1024 },
    @{ name = "icon_180.png"; size = 180 },
    @{ name = "icon_120.png"; size = 120 },
    @{ name = "icon_87.png"; size = 87 },
    @{ name = "icon_80.png"; size = 80 },
    @{ name = "icon_60.png"; size = 60 },
    @{ name = "icon_58.png"; size = 58 },
    @{ name = "icon_40.png"; size = 40 },
    @{ name = "icon_29.png"; size = 29 },
    @{ name = "icon_20.png"; size = 20 }
)

foreach ($item in $sizes) {
    $bmp = New-Object System.Drawing.Bitmap $item.size, $item.size
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.DrawImage($img, 0, 0, $item.size, $item.size)
    $bmp.Save((Join-Path $destDir $item.name), [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $bmp.Dispose()
}

$img.Dispose()
Write-Host "Icons generated successfully!"
