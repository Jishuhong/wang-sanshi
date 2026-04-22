# ToTng Image Crop Script
# Uses PowerShell + System.Drawing to crop gun skin images

Add-Type -AssemblyName System.Drawing

$rawDir = "D:\AI\totng-site\assets\raw"
$skinsDir = "D:\AI\totng-site\assets\skins"
$cardsDir = "D:\AI\totng-site\assets\cards"
$dataDir = "D:\AI\totng-site\assets\data"

# Ensure output directories exist
$null = New-Item -ItemType Directory -Force -Path $skinsDir
$null = New-Item -ItemType Directory -Force -Path $cardsDir
$null = New-Item -ItemType Directory -Force -Path $dataDir

Write-Host "========================================"
Write-Host "ToTng Image Crop Tool"
Write-Host "========================================"

# Get all jpg files
$files = Get-ChildItem -Path $rawDir -Filter "*.jpg"
Write-Host "Found $($files.Count) jpg files"

# Find gun skin files (larger files)
$gunskin1 = $files | Where-Object { $_.Length -gt 600000 } | Select-Object -First 1
$gunskin2 = $files | Where-Object { $_.Length -gt 600000 } | Select-Object -Last 1
$totngHome = $files | Where-Object { $_.Length -gt 400000 -and $_.Length -lt 500000 } | Select-Object -First 1

Write-Host "Gun skin 1: $($gunskin1.Name)"
Write-Host "Gun skin 2: $($gunskin2.Name)"
Write-Host "ToTng home: $($totngHome.Name)"

# Crop gun skin 1 - Chroma 5 guns
Write-Host "`n--- Cropping Gun Skin 1 (Chroma Series) ---"
$img1 = [System.Drawing.Image]::FromFile($gunskin1.FullName)
$w1 = $img1.Width
$h1 = $img1.Height
$skinHeight = [int]($h1 / 5)

$skinNames = @('Operator', 'Vandal', 'Sheriff', 'Phantom', 'Spectre')
Write-Host "Image size: ${w1}x${h1}, each section height: $skinHeight"

for ($i = 0; $i -lt 5; $i++) {
    $y = [int]($skinHeight * $i)
    $rect = New-Object System.Drawing.Rectangle(0, $y, $w1, $skinHeight)
    $region = $img1.Clone($rect, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
    $outputPath = Join-Path $skinsDir "chroma_$($skinNames[$i]).jpg"
    $region.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
    Write-Host "  Saved: chroma_$($skinNames[$i]).jpg"
    $region.Dispose()
}
$img1.Dispose()

# Crop gun skin 2 - RG Collection + cards
Write-Host "`n--- Cropping Gun Skin 2 (RG + Cards) ---"
$img2 = [System.Drawing.Image]::FromFile($gunskin2.FullName)
$w2 = $img2.Width
$h2 = $img2.Height
$quarter = [int]($h2 / 4)

Write-Host "Image size: ${w2}x${h2}, each section height: $quarter"

# RG guns
$rgNames = @('RG_Vandal', 'RG_Operator')
for ($i = 0; $i -lt 2; $i++) {
    $y = [int]($quarter * $i)
    $rect = New-Object System.Drawing.Rectangle(0, $y, $w2, $quarter)
    $region = $img2.Clone($rect, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
    $outputPath = Join-Path $skinsDir "$($rgNames[$i]).jpg"
    $region.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
    Write-Host "  Saved: $($rgNames[$i]).jpg"
    $region.Dispose()
}

# Cards
$cardNames = @('Sova', 'Killjoy')
for ($i = 0; $i -lt 2; $i++) {
    $y = [int]($quarter * ($i + 2))
    $rect = New-Object System.Drawing.Rectangle(0, $y, $w2, $quarter)
    $region = $img2.Clone($rect, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
    $outputPath = Join-Path $cardsDir "$($cardNames[$i]).jpg"
    $region.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
    Write-Host "  Saved: $($cardNames[$i]).jpg"
    $region.Dispose()
}
$img2.Dispose()

# Crop avatar from ToTng home image
Write-Host "`n--- Cropping ToTng Avatar ---"
$img3 = [System.Drawing.Image]::FromFile($totngHome.FullName)
$w3 = $img3.Width
$h3 = $img3.Height

$avatarX = [int]($w3 * 0.25)
$avatarY = [int]($h3 * 0.1)
$avatarW = [int]($w3 * 0.5)
$avatarH = [int]($h3 * 0.3)

$rect = New-Object System.Drawing.Rectangle($avatarX, $avatarY, $avatarW, $avatarH)
$avatar = $img3.Clone($rect, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
$resized = New-Object System.Drawing.Bitmap($avatar, 300, 300)
$outputPath = Join-Path $dataDir "avatar_totng.jpg"
$resized.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
Write-Host "  Saved: avatar_totng.jpg (300x300)"

$avatar.Dispose()
$resized.Dispose()
$img3.Dispose()

# Process data screenshots
Write-Host "`n--- Processing Data Images ---"
$dataFiles = $files | Where-Object { $_.Name -match '^[0-9a-f]{32}\.jpg$' } | Select-Object -First 4

foreach ($file in $dataFiles) {
    Write-Host "Processing: $($file.Name)"
    $img = [System.Drawing.Image]::FromFile($file.FullName)
    $w = $img.Width
    $h = $img.Height

    $cropX = [int]($w * 0.1)
    $cropY = [int]($h * 0.2)
    $cropW = [int]($w * 0.8)
    $cropH = [int]($h * 0.5)

    $rect = New-Object System.Drawing.Rectangle($cropX, $cropY, $cropW, $cropH)
    $cropped = $img.Clone($rect, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
    $outputPath = Join-Path $dataDir "data_$($file.Name)"
    $cropped.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
    Write-Host "  Saved: data_$($file.Name)"

    $cropped.Dispose()
    $img.Dispose()
}

Write-Host "`n========================================"
Write-Host "Done! All images cropped and saved"
Write-Host "========================================"
Write-Host "`nOutput directories:"
Write-Host "  Skins: $skinsDir"
Write-Host "  Cards: $cardsDir"
Write-Host "  Data/Avatar: $dataDir"
