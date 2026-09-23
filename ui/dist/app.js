(async function () {
  const hostMeta = document.getElementById("hostMeta");
  const list = document.getElementById("profiles");
  let state = {
    version: "2.2.1",
    lastUsed: "",
    profiles: [],
    selectedProfile: "",
    openClassic: false,
    saveOverview: false
  };

  function selectedProfile() {
    return (state.profiles || []).find(function (p) {
      return p.name === state.selectedProfile;
    });
  }

  function fillOverview() {
    const p = selectedProfile();
    if (!p) return;
    document.getElementById("baseFolder").value = p.baseFolder || "";
    document.querySelectorAll('input[name="mode"]').forEach(function (el) {
      el.checked = el.value === (p.mode || "Move");
    });
    document.getElementById("useFolder").checked = !!p.useFolder;
    document.getElementById("useFileName").checked = !!p.useFileName;
    document.getElementById("copyMode").checked = !!p.copyMode;
    document.getElementById("moveFileless").checked = !!p.moveFileless;
  }

  function readOverviewIntoState() {
    const p = selectedProfile();
    if (!p) return;
    p.baseFolder = document.getElementById("baseFolder").value || "";
    const modeEl = document.querySelector('input[name="mode"]:checked');
    p.mode = modeEl ? modeEl.value : "Move";
    p.useFolder = document.getElementById("useFolder").checked;
    p.useFileName = document.getElementById("useFileName").checked;
    p.copyMode = document.getElementById("copyMode").checked;
    p.moveFileless = document.getElementById("moveFileless").checked;
  }

  function render() {
    list.innerHTML = "";
    (state.profiles || []).forEach(function (p) {
      const li = document.createElement("li");
      li.textContent = p.name + (p.baseFolder ? " — " + p.baseFolder : "");
      if (p.name === state.selectedProfile) li.className = "active";
      li.addEventListener("click", async function () {
        readOverviewIntoState();
        state.selectedProfile = p.name;
        fillOverview();
        render();
        await HostApi.call("host.config.set", { config: JSON.stringify(state) });
      });
      list.appendChild(li);
    });
    if (!list.children.length) {
      const li = document.createElement("li");
      li.textContent = "No profiles found.";
      list.appendChild(li);
    }
  }

  async function persist(extra) {
    readOverviewIntoState();
    Object.assign(state, extra || {});
    await HostApi.call("host.config.set", { config: JSON.stringify(state) });
  }

  try {
    const info = await HostApi.call("host.getInfo");
    hostMeta.textContent =
      "Host " + info.productVersion + " · API v" + info.apiVersion + " · SPA Configure Phase B";

    const cfg = await HostApi.call("host.config.get");
    if (cfg && cfg.config) {
      try {
        state = Object.assign(state, JSON.parse(cfg.config));
      } catch (e) {
        hostMeta.textContent += " (bridge parse warning)";
      }
    }
    if (!state.selectedProfile && state.lastUsed) state.selectedProfile = state.lastUsed;
    if (!state.selectedProfile && state.profiles && state.profiles[0]) {
      state.selectedProfile = state.profiles[0].name;
    }
    render();
    fillOverview();
  } catch (err) {
    hostMeta.textContent = "Host bridge error: " + (err.message || JSON.stringify(err));
  }

  document.getElementById("btnSave").addEventListener("click", async function () {
    await persist({ saveOverview: true, openClassic: false });
    await HostApi.call("host.ui.close", { dialogResult: "ok" });
  });
  document.getElementById("btnClassic").addEventListener("click", async function () {
    await persist({ openClassic: true, saveOverview: false });
    await HostApi.call("host.ui.close", { dialogResult: "ok" });
  });
  document.getElementById("btnClose").addEventListener("click", async function () {
    await persist({ openClassic: false, saveOverview: false });
    await HostApi.call("host.ui.close", { dialogResult: "ok" });
  });
})();
