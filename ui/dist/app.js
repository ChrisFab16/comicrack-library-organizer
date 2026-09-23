(async function () {
  const hostMeta = document.getElementById("hostMeta");
  const list = document.getElementById("profiles");
  const selectedEl = document.getElementById("selected");
  let state = {
    version: "2.2.0",
    lastUsed: "",
    profiles: [],
    selectedProfile: "",
    openClassic: false
  };

  function render() {
    list.innerHTML = "";
    (state.profiles || []).forEach(function (p) {
      const li = document.createElement("li");
      li.textContent = p.name + (p.baseFolder ? " — " + p.baseFolder : "");
      if (p.name === state.selectedProfile) li.className = "active";
      li.addEventListener("click", async function () {
        state.selectedProfile = p.name;
        selectedEl.textContent = "Selected: " + p.name;
        render();
        await HostApi.call("host.config.set", { config: JSON.stringify(state) });
      });
      list.appendChild(li);
    });
    if (!list.children.length) {
      const li = document.createElement("li");
      li.textContent = "No profiles found (bridge empty).";
      list.appendChild(li);
    }
    selectedEl.textContent = state.selectedProfile
      ? "Selected: " + state.selectedProfile
      : "";
  }

  try {
    const info = await HostApi.call("host.getInfo");
    hostMeta.textContent =
      "Host " + info.productVersion + " · API v" + info.apiVersion + " · SPA Configure Phase A";

    const cfg = await HostApi.call("host.config.get");
    if (cfg && cfg.config) {
      try {
        state = Object.assign(state, JSON.parse(cfg.config));
      } catch (e) {
        hostMeta.textContent += " (bridge parse warning)";
      }
    }
    if (!state.selectedProfile && state.lastUsed) state.selectedProfile = state.lastUsed;
    render();
  } catch (err) {
    hostMeta.textContent = "Host bridge error: " + (err.message || JSON.stringify(err));
  }

  document.getElementById("btnClassic").addEventListener("click", async function () {
    state.openClassic = true;
    await HostApi.call("host.config.set", { config: JSON.stringify(state) });
    await HostApi.call("host.ui.close", { dialogResult: "ok" });
  });
  document.getElementById("btnClose").addEventListener("click", async function () {
    state.openClassic = false;
    await HostApi.call("host.config.set", { config: JSON.stringify(state) });
    await HostApi.call("host.ui.close", { dialogResult: "ok" });
  });
})();
