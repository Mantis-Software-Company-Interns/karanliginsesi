const oyunDurumu = {
  karakterTuru: null,
  karakterAdi: null,
  hikayeMetni: "",
  aktif: false
};

function ekranGoster(ekranId) {
  document.getElementById("karakter-secim-ekrani").style.display = "none";
  document.getElementById("oyun-ekrani").style.display = "none";
  document.getElementById("olum-ekrani").style.display = "none";
  document.getElementById(ekranId).style.display = "block";
}

function yukleniyorGoster(durum) {
  document.getElementById("yukleniyor-gostergesi").style.display = durum ? "block" : "none";
  document.querySelectorAll(".aksiyon-btn").forEach(btn => btn.disabled = durum);
}

function sahneEkle(metin) {
  const kutu = document.getElementById("hikaye-kutusu");
  const p = document.createElement("p");
  p.textContent = metin;
  kutu.appendChild(p);
  kutu.scrollTop = kutu.scrollHeight;
  oyunDurumu.hikayeMetni += metin + "\n";
}

function aksiyonlarGuncelle(aksiyonlar) {
  aksiyonlar.forEach((aksiyon, i) => {
    const btn = document.getElementById(`aksiyon-btn-${i}`);
    btn.textContent = aksiyon;
    btn.disabled = false;
  });
}

async function karakterSec(tur) {
  if (oyunDurumu.aktif) return;
  oyunDurumu.aktif = true;
  yukleniyorGoster(true);
  try {
    const response = await fetch("/api/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ karakterTuru: tur })
    });
    if (!response.ok) throw new Error("Sunucu hatası");
    const data = await response.json();
    oyunDurumu.karakterTuru = tur;
    oyunDurumu.karakterAdi = data.karakterAdi;
    document.title = "Karanligin Sesi - " + data.karakterAdi;
    document.getElementById("karakter-adi").textContent = data.karakterAdi;
    document.getElementById("karakter-arkaplan").textContent = data.karakterArkaplan;
    document.getElementById("karakter-dt").textContent = "Doğum: " + data.karakterDt;
    sahneEkle(data.olaylar);
    aksiyonlarGuncelle(data.muhtemelAksiyonlar);
    ekranGoster("oyun-ekrani");
  } catch (error) {
    alert("Hata: " + error.message);
  } finally {
    yukleniyorGoster(false);
    oyunDurumu.aktif = false;
  }
}

async function aksiyonSec(aksiyonMetni) {
  if (oyunDurumu.aktif) return;
  oyunDurumu.aktif = true;
  yukleniyorGoster(true);
  sahneEkle("→ " + aksiyonMetni);
  try {
    const response = await fetch("/api/action", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        aksiyonu: aksiyonMetni,
        hikayeMetni: oyunDurumu.hikayeMetni
      })
    });
    if (!response.ok) throw new Error("Sunucu hatası");
    const data = await response.json();
    sahneEkle(data.olaylar);
    if (data.oldu) {
      document.getElementById("son-sahne").textContent = oyunDurumu.hikayeMetni;
      ekranGoster("olum-ekrani");
    } else {
      aksiyonlarGuncelle(data.muhtemelAksiyonlar);
    }
  } catch (error) {
    const kutu = document.getElementById("hikaye-kutusu");
    const p = document.createElement("p");
    p.textContent = "Hata: " + error.message;
    kutu.appendChild(p);
  } finally {
    yukleniyorGoster(false);
    oyunDurumu.aktif = false;
  }
}

function yenidenBasla() {
  oyunDurumu.karakterTuru = null;
  oyunDurumu.karakterAdi = null;
  oyunDurumu.hikayeMetni = "";
  oyunDurumu.aktif = false;
  document.title = "Karanligin Sesi";
  document.getElementById("hikaye-kutusu").innerHTML = "";
  ekranGoster("karakter-secim-ekrani");
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".karakter-karti").forEach(kart => {
    kart.addEventListener("click", () => karakterSec(kart.dataset.tur));
  });
  document.querySelectorAll(".aksiyon-btn").forEach(btn => {
    btn.addEventListener("click", () => aksiyonSec(btn.textContent));
  });
  document.getElementById("yeniden-basla-btn").addEventListener("click", yenidenBasla);
});
