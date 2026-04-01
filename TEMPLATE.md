<div align="center">

<!-- HEADER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:161b22,100:58a6ff&height=220&section=header&text=Hey,%20I'm%20Frankie%20👋&fontSize=42&fontColor=ffffff&fontAlignY=35&desc=Platform%20Engineer%20·%20Building%20resilient%20infrastructure&descSize=18&descAlignY=55&descColor=8b949e&animation=fadeIn" width="100%" />

<!-- LIVE CLOCK -->
<p>
<img src="https://img.shields.io/badge/📅_Today-{{date}}-58a6ff?style=for-the-badge&labelColor=0d1117" />
<img src="https://img.shields.io/badge/☕_Visitors-welcome-f78166?style=for-the-badge&labelColor=0d1117" />
</p>

<a href="https://github.com/francescowang"><img src="https://komarev.com/ghpvc/?username=francescowang&style=for-the-badge&color=58a6ff&label=PROFILE+VIEWS" /></a>

</div>

---

<!-- ABOUT ME -->
## 🧬 About Me

```yaml
name: Frankie
role: Platform Engineer
location: 🌍 Earth
focus:
  - Cloud-native infrastructure
  - Developer experience & platform engineering
  - Reliability & observability at scale
  - Infrastructure as Code
motto: "Automate everything. Monitor the rest."
currently_learning: [ "eBPF", "WebAssembly", "Nix" ]
fun_fact: "This README updates itself every day via GitHub Actions ⚡"
```

---

<!-- TECH STACK -->
## 🛠️ Tech Stack & Arsenal

<details open>
<summary><b>☁️ Cloud & Infrastructure</b></summary>
<br/>
<p>
<img src="https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" />
<img src="https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white" />
<img src="https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white" />
<img src="https://img.shields.io/badge/Ansible-EE0000?style=for-the-badge&logo=ansible&logoColor=white" />
</p>
</details>

<details open>
<summary><b>🐳 Containers & Orchestration</b></summary>
<br/>
<p>
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
<img src="https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" />
<img src="https://img.shields.io/badge/Helm-0F1689?style=for-the-badge&logo=helm&logoColor=white" />
</p>
</details>

<details open>
<summary><b>🔄 CI/CD & Automation</b></summary>
<br/>
<p>
<img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" />
<img src="https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white" />
<img src="https://img.shields.io/badge/ArgoCD-EF7B4D?style=for-the-badge&logo=argo&logoColor=white" />
</p>
</details>

<details open>
<summary><b>📊 Monitoring & Observability</b></summary>
<br/>
<p>
<img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white" />
<img src="https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white" />
<img src="https://img.shields.io/badge/Datadog-632CA6?style=for-the-badge&logo=datadog&logoColor=white" />
</p>
</details>

<details open>
<summary><b>💻 Languages & Tools</b></summary>
<br/>
<p>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white" />
<img src="https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white" />
<img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" />
<img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" />
<img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" />
</p>
</details>

<details open>
<summary><b>🗄️ Databases</b></summary>
<br/>
<p>
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
<img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" />
</p>
</details>

---

<!-- LIVE WEATHER DASHBOARD -->
## 🌤️ World Weather Dashboard

> *Live weather across major cities — updated daily via GitHub Actions*

<table>
<tr>
<th>🏙️ City</th>
<th>🌡️ Temp</th>
<th>💧 Humidity</th>
<th>🌬️ Wind</th>
<th>☁️ Conditions</th>
</tr>
{{weather_rows}}
</table>

<sub>🕐 Last weather update: <b>{{weather_update_time}}</b></sub>

---

<!-- STOCK / ETF TRACKER -->
## 📈 ETF & Market Watch

> *Tracking some ETFs for fun — not financial advice!*

<table>
<tr>
<th>📊 Ticker</th>
<th>💰 Price</th>
<th>📉 Change</th>
<th>📊 % Change</th>
<th>📅 As Of</th>
</tr>
{{stock_rows}}
</table>

<sub>🕐 Last market update: <b>{{stock_update_time}}</b> · Data from Yahoo Finance</sub>

---

<!-- DAILY BRAIN FOOD -->
## 🧠 Daily Brain Food

<table>
<tr>
<td width="50%">

### 📖 Word of the Day

> **{{word}}** · *{{word_pronunciation}}*
>
> *{{word_type}}* — {{word_meaning}}
>
> 💬 *"{{word_example}}"*

</td>
<td width="50%">

### 🏛️ Philosopher's Quote

> *"{{philosopher_quote}}"*
>
> — **{{philosopher_author}}**

</td>
</tr>
<tr>
<td>

### {{fun_fact_emoji}} Fun Fact

> {{fun_fact}}

</td>
<td>

### 🌙 Moon Phase

> {{moon_phase}}

### {{history_emoji}} On This Day ({{today_month_day}})

> **{{history_year}}** — {{history_event}}

</td>
</tr>
</table>

---

<!-- COUNTDOWN -->
## ⏳ Countdown to Fun Events

| 🎉 Event | 📅 Days Left |
|-----------|-------------|
{{countdowns}}

---

<!-- GITHUB STATS -->
## 📊 GitHub Stats

<div align="center">
<a href="https://github.com/francescowang">
<img height="180em" src="https://github-readme-stats.vercel.app/api?username=francescowang&show_icons=true&theme=github_dark&hide_border=true&bg_color=0d1117&title_color=58a6ff&icon_color=58a6ff&text_color=c9d1d9&ring_color=58a6ff" />
<img height="180em" src="https://github-readme-stats.vercel.app/api/top-langs/?username=francescowang&layout=compact&theme=github_dark&hide_border=true&bg_color=0d1117&title_color=58a6ff&text_color=c9d1d9" />
</a>
</div>

<div align="center">
<img src="https://github-readme-streak-stats.herokuapp.com?user=francescowang&theme=github-dark-blue&hide_border=true&background=0D1117&ring=58A6FF&fire=58A6FF&currStreakLabel=58A6FF" />
</div>

---

<!-- CONTRIBUTION GRAPH -->
## 🐍 Contribution Snake

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/francescowang/francescowang/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/francescowang/francescowang/output/github-snake.svg" />
  <img alt="github contribution snake animation" src="https://raw.githubusercontent.com/francescowang/francescowang/output/github-snake-dark.svg" />
</picture>
</div>

---

<!-- RANDOM QUOTE -->
## 💡 Dev Quote of the Day

<div align="center">
<img src="https://quotes-github-readme.vercel.app/api?type=horizontal&theme=dark" />
</div>

---

<!-- CONNECT -->
## 🤝 Let's Connect

<div align="center">
<a href="https://github.com/francescowang"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" /></a>
<a href="https://linkedin.com/in/francescowang"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" /></a>
</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:161b22,100:58a6ff&height=120&section=footer" width="100%" />

<sub>⚡ This README is <b>auto-generated</b> daily by <a href="https://github.com/francescowang/francescowang/blob/main/.github/workflows/update-readme.yml">GitHub Actions</a> · Powered by Mustache templating</sub>

</div>
