// ===== Edit these before launch =====
const CONFIG = {
  contract: "", // e.g. "nightwing.tkn.near" — leave empty to show "coming soon"
  links: {
    buy: "#buy",
    dex: "https://app.ref.finance/",
    chart: "https://dexscreener.com/near",
    x: "https://x.com/",
    telegram: "https://t.me/",
  },
};
// ====================================

document.querySelectorAll("[data-link]").forEach((a) => {
  const url = CONFIG.links[a.dataset.link];
  if (!url) return;
  a.href = url;
  if (url.startsWith("http")) { a.target = "_blank"; a.rel = "noopener"; }
});

const caEl = document.getElementById("ca");
const copyBtn = document.getElementById("copy");
if (CONFIG.contract) caEl.textContent = CONFIG.contract;
else copyBtn.hidden = true;
copyBtn.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(CONFIG.contract);
    copyBtn.textContent = "Copied!";
  } catch {
    copyBtn.textContent = "Select & copy";
  }
  setTimeout(() => (copyBtn.textContent = "Copy"), 1500);
});

document.getElementById("year").textContent = new Date().getFullYear();

// Fade sections in on scroll
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => e.isIntersecting && (e.target.classList.add("in"), io.unobserve(e.target)));
}, { threshold: 0.12 });
document.querySelectorAll(".section").forEach((s) => { s.classList.add("reveal"); io.observe(s); });

// Twinkling night sky
const c = document.getElementById("stars");
const ctx = c.getContext("2d");
let stars = [];
function resize() {
  c.width = innerWidth * devicePixelRatio;
  c.height = innerHeight * devicePixelRatio;
  stars = Array.from({ length: Math.round(innerWidth / 8) }, () => ({
    x: Math.random() * c.width, y: Math.random() * c.height,
    r: Math.random() * 1.4 * devicePixelRatio + 0.3, p: Math.random() * Math.PI * 2,
  }));
}
function draw(t) {
  ctx.clearRect(0, 0, c.width, c.height);
  for (const s of stars) {
    ctx.globalAlpha = 0.35 + 0.35 * Math.sin(t / 900 + s.p);
    ctx.fillStyle = "#cfe0ff";
    ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2); ctx.fill();
  }
  if (!matchMedia("(prefers-reduced-motion: reduce)").matches) requestAnimationFrame(draw);
}
addEventListener("resize", resize);
resize();
requestAnimationFrame(draw);
