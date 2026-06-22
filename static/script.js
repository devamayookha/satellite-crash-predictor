// ── Starfield ──────────────────────────────────────────────
const canvas = document.getElementById("starfield");
const ctx    = canvas.getContext("2d");

function resizeCanvas() {
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener("resize", resizeCanvas);

const stars = Array.from({ length: 160 }, () => ({
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    r: Math.random() * 1.2 + 0.2,
    o: Math.random() * 0.5 + 0.1,
    speed: Math.random() * 0.3 + 0.05,
}));

function drawStars() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    stars.forEach(s => {
        s.o += s.speed * 0.01 * (Math.random() > 0.5 ? 1 : -1);
        s.o = Math.max(0.05, Math.min(0.7, s.o));
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(180, 200, 255, ${s.o})`;
        ctx.fill();
    });
    requestAnimationFrame(drawStars);
}
drawStars();

// ── Assessment ─────────────────────────────────────────────
document.getElementById("assess-btn").addEventListener("click", async () => {
    const btn     = document.getElementById("assess-btn");
    const btnText = document.getElementById("btn-text");

    const fields = ["altitude1", "altitude2", "velocity", "miss_distance", "time_to_approach"];
    for (const id of fields) {
        if (document.getElementById(id).value === "") {
            alert("Please fill in all fields before running the assessment.");
            return;
        }
    }

    btnText.textContent = "PROCESSING...";
    btn.disabled = true;

    const payload = {
        altitude1:        document.getElementById("altitude1").value,
        altitude2:        document.getElementById("altitude2").value,
        velocity:         document.getElementById("velocity").value,
        miss_distance:    document.getElementById("miss_distance").value,
        size_category:    document.getElementById("size_category").value,
        time_to_approach: document.getElementById("time_to_approach").value,
    };

    const response = await fetch("/predict", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify(payload),
    });

    const result = await response.json();

    document.getElementById("empty-state").style.display    = "none";
    document.getElementById("result-content").style.display = "block";

    const badge = document.getElementById("risk-badge");
    badge.className = "risk-badge " + result.risk_level;
    document.getElementById("risk-label").textContent = result.risk_level.toUpperCase();

    document.getElementById("score-number").textContent = result.risk_score + "/100";
    const fill = document.getElementById("score-bar-fill");
    fill.className = "score-bar-fill " + result.risk_level;
    setTimeout(() => { fill.style.width = result.risk_score + "%"; }, 50);

    document.getElementById("action-text").textContent      = result.action;
    document.getElementById("explanation-text").textContent = result.explanation;

    btnText.textContent = "RUN ASSESSMENT";
    btn.disabled = false;
});