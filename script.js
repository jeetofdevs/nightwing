// ===== Edit these before launch =====
const CONFIG = {
  launched: true, // true = buy buttons link to links.buy; false = "Coming Soon"
  contract: "nightwing.v2-launchpad.justhoot.near",
  links: {
    buy: "https://justhoot.fun/p/nightwing.v2-launchpad.justhoot.near",
    x: "https://x.com/NightwingOnNear",
  },
};
// ====================================

const TRADE_LINKS = ["buy"];
document.querySelectorAll("[data-link]").forEach((a) => {
  const key = a.dataset.link;
  if (TRADE_LINKS.includes(key) && (!CONFIG.launched || !CONFIG.links[key])) {
    a.textContent = "Buy — Coming Soon";
    a.removeAttribute("href");
    a.setAttribute("aria-disabled", "true");
    a.classList.add("soon");
    return;
  }
  const url = CONFIG.links[key];
  if (!url) { a.hidden = true; return; }
  if (key === "buy") {               // launched: turn the placeholder into a real button
    a.textContent = "Buy $NIGHTWING";
    a.classList.remove("soon");
    a.removeAttribute("aria-disabled");
  }
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
