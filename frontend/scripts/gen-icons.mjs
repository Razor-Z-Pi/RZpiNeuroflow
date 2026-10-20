import sharp from "sharp";
import { mkdirSync } from "node:fs";

mkdirSync("public/icons", { recursive: true });

const svg = `
<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="96" fill="#0B0F1A"/>
  <circle cx="256" cy="256" r="140" fill="none" stroke="#B4FF39" stroke-width="14" opacity="0.2"/>
  <circle cx="256" cy="256" r="90" fill="none" stroke="#B4FF39" stroke-width="14" opacity="0.5"/>
  <circle cx="256" cy="256" r="40" fill="#B4FF39"/>
</svg>
`;

for (const size of [192, 512]) {
  await sharp(Buffer.from(svg))
    .resize(size, size)
    .png()
    .toFile(`public/icons/icon-${size}.png`);
  console.log(`icon-${size}.png created`);
}