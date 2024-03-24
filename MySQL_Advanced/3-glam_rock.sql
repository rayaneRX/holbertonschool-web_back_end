--  lists all bands with Glam rock
SELECT band_name, 2024 - formed AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;