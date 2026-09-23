(async function () {
  // Catalogs mirrored from configureform.py empty_substitution_items / failed_items
  // and locommon.name_to_field for those labels.
  const LABEL_TO_FIELD = {
    "Age Rating": "AgeRating",
    "Alternate Count": "AlternateCount",
    "Alternate Number": "AlternateNumber",
    "Alternate Series": "AlternateSeries",
    "Black And White": "BlackAndWhite",
    Characters: "Characters",
    Colorist: "Colorist",
    Count: "ShadowCount",
    "Cover Artist": "CoverArtist",
    Editor: "Editor",
    Format: "ShadowFormat",
    "First Letter": "FirstLetter",
    Genre: "Genre",
    Imprint: "Imprint",
    Inker: "Inker",
    Language: "LanguageISO",
    Letterer: "Letterer",
    Locations: "Locations",
    "Main Character Or Team": "MainCharacterOrTeam",
    Manga: "Manga",
    Month: "Month",
    Notes: "Notes",
    Number: "ShadowNumber",
    Penciller: "Penciller",
    Publisher: "Publisher",
    Rating: "Rating",
    "Read Percentage": "ReadPercentage",
    Review: "Review",
    "Scan Information": "ScanInformation",
    Series: "ShadowSeries",
    "Series Complete": "SeriesComplete",
    "Series Group": "SeriesGroup",
    "Start Month": "StartMonth",
    "Start Year": "StartYear",
    "Story Arc": "StoryArc",
    Tags: "Tags",
    Teams: "Teams",
    Title: "ShadowTitle",
    Volume: "ShadowVolume",
    Web: "Web",
    Writer: "Writer",
    Year: "ShadowYear"
  };

  const SUBSTITUTION_LABELS = [
    "Age Rating", "Alternate Count", "Alternate Number", "Alternate Series", "Black And White",
    "Characters", "Colorist", "Count", "Cover Artist", "Editor", "Format", "First Letter", "Genre",
    "Imprint", "Inker", "Language", "Letterer", "Locations", "Main Character Or Team", "Manga",
    "Month", "Number", "Penciller", "Publisher", "Rating", "Read Percentage", "Scan Information",
    "Series", "Series Complete", "Series Group", "Start Month", "Start Year", "Story Arc", "Tags",
    "Teams", "Title", "Volume", "Writer", "Year"
  ];

  const FAILED_LABELS = [
    "Age Rating", "Alternate Count", "Alternate Number", "Alternate Series", "Black And White",
    "Characters", "Colorist", "Count", "Cover Artist", "Editor", "Format", "Genre", "Imprint",
    "Inker", "Language", "Letterer", "Locations", "Main Character Or Team", "Manga", "Month",
    "Notes", "Number", "Penciller", "Publisher", "Rating", "Read Percentage", "Review",
    "Scan Information", "Series", "Series Complete", "Series Group", "Start Month", "Start Year",
    "Story Arc", "Tags", "Teams", "Title", "Volume", "Web", "Writer", "Year"
  ];

  const hostMeta = document.getElementById("hostMeta");
  const list = document.getElementById("profiles");
  let state = {
    version: "2.2.3",
    lastUsed: "",
    profiles: [],
    selectedProfile: "",
    openClassic: false,
    saveOverview: false
  };
  let lastEmptyField = null;

  function selectedProfile() {
    return (state.profiles || []).find(function (p) {
      return p.name === state.selectedProfile;
    });
  }

  function ensureProfileShapes(p) {
    if (!p.emptyData || typeof p.emptyData !== "object" || Array.isArray(p.emptyData)) {
      const map = {};
      if (Array.isArray(p.emptyData)) {
        p.emptyData.forEach(function (row) {
          if (row && row.field) map[row.field] = row.value || "";
        });
      }
      p.emptyData = map;
    }
    if (!Array.isArray(p.failedFields)) p.failedFields = [];
    if (!Array.isArray(p.excludedEmptyFolder)) p.excludedEmptyFolder = [];
  }

  function emptyDataToBridgeArray(map) {
    const out = [];
    Object.keys(map || {}).forEach(function (field) {
      out.push({ field: field, value: map[field] == null ? "" : String(map[field]) });
    });
    return out;
  }

  function fillEmptyFieldSelect() {
    const sel = document.getElementById("emptyField");
    if (sel.options.length) return;
    SUBSTITUTION_LABELS.forEach(function (label) {
      const opt = document.createElement("option");
      opt.value = LABEL_TO_FIELD[label];
      opt.textContent = label;
      sel.appendChild(opt);
    });
  }

  function renderFailedChecklist() {
    const root = document.getElementById("failedFields");
    const p = selectedProfile();
    root.innerHTML = "";
    if (!p) return;
    ensureProfileShapes(p);
    FAILED_LABELS.forEach(function (label) {
      const field = LABEL_TO_FIELD[label];
      const lab = document.createElement("label");
      lab.className = "check";
      const cb = document.createElement("input");
      cb.type = "checkbox";
      cb.dataset.field = field;
      cb.checked = p.failedFields.indexOf(field) >= 0;
      cb.addEventListener("change", function () {
        readFailedFieldsIntoState();
      });
      lab.appendChild(cb);
      lab.appendChild(document.createTextNode(" " + label));
      root.appendChild(lab);
    });
  }

  function renderExcludedList() {
    const ul = document.getElementById("excludedList");
    const p = selectedProfile();
    ul.innerHTML = "";
    if (!p) return;
    ensureProfileShapes(p);
    p.excludedEmptyFolder.forEach(function (path, idx) {
      const li = document.createElement("li");
      li.textContent = path;
      const rm = document.createElement("button");
      rm.type = "button";
      rm.className = "secondary tiny";
      rm.textContent = "Remove";
      rm.addEventListener("click", function () {
        p.excludedEmptyFolder.splice(idx, 1);
        renderExcludedList();
      });
      li.appendChild(rm);
      ul.appendChild(li);
    });
    if (!p.excludedEmptyFolder.length) {
      const li = document.createElement("li");
      li.className = "muted";
      li.textContent = "No exceptions.";
      ul.appendChild(li);
    }
  }

  function fillEmptyForm() {
    const p = selectedProfile();
    if (!p) return;
    ensureProfileShapes(p);
    fillEmptyFieldSelect();
    const field = document.getElementById("emptyField").value;
    document.getElementById("emptyValue").value = (p.emptyData && p.emptyData[field]) || "";
    lastEmptyField = field;
    renderFailedChecklist();
    renderExcludedList();
  }

  function readFailedFieldsIntoState() {
    const p = selectedProfile();
    if (!p) return;
    ensureProfileShapes(p);
    const next = [];
    document.querySelectorAll("#failedFields input[type=checkbox]").forEach(function (cb) {
      if (cb.checked) next.push(cb.dataset.field);
    });
    p.failedFields = next;
  }

  function fillForm() {
    const p = selectedProfile();
    if (!p) return;
    ensureProfileShapes(p);
    document.getElementById("baseFolder").value = p.baseFolder || "";
    document.querySelectorAll('input[name="mode"]').forEach(function (el) {
      el.checked = el.value === (p.mode || "Move");
    });
    document.getElementById("useFolder").checked = !!p.useFolder;
    document.getElementById("useFileName").checked = !!p.useFileName;
    document.getElementById("copyMode").checked = !!p.copyMode;
    document.getElementById("moveFileless").checked = !!p.moveFileless;
    document.getElementById("dontAskWhenMultiOne").checked = p.dontAskWhenMultiOne !== false;
    document.getElementById("removeEmptyFolder").checked = p.removeEmptyFolder !== false;
    document.getElementById("emptyFolder").value = p.emptyFolder || "";
    document.getElementById("filelessFormat").value = p.filelessFormat || ".jpg";
    document.getElementById("failEmptyValues").checked = !!p.failEmptyValues;
    document.getElementById("moveFailed").checked = !!p.moveFailed;
    document.getElementById("failedFolder").value = p.failedFolder || "";
    fillEmptyForm();
  }

  function readFormIntoState() {
    const p = selectedProfile();
    if (!p) return;
    ensureProfileShapes(p);
    p.baseFolder = document.getElementById("baseFolder").value || "";
    const modeEl = document.querySelector('input[name="mode"]:checked');
    p.mode = modeEl ? modeEl.value : "Move";
    p.useFolder = document.getElementById("useFolder").checked;
    p.useFileName = document.getElementById("useFileName").checked;
    p.copyMode = document.getElementById("copyMode").checked;
    p.moveFileless = document.getElementById("moveFileless").checked;
    p.dontAskWhenMultiOne = document.getElementById("dontAskWhenMultiOne").checked;
    p.removeEmptyFolder = document.getElementById("removeEmptyFolder").checked;
    p.emptyFolder = document.getElementById("emptyFolder").value || "";
    p.filelessFormat = document.getElementById("filelessFormat").value || ".jpg";
    p.failEmptyValues = document.getElementById("failEmptyValues").checked;
    p.moveFailed = document.getElementById("moveFailed").checked;
    p.failedFolder = document.getElementById("failedFolder").value || "";
    const field = document.getElementById("emptyField").value;
    p.emptyData[field] = document.getElementById("emptyValue").value || "";
    readFailedFieldsIntoState();
  }

  function profilesForBridge() {
    return (state.profiles || []).map(function (p) {
      ensureProfileShapes(p);
      const copy = Object.assign({}, p);
      copy.emptyData = emptyDataToBridgeArray(p.emptyData);
      return copy;
    });
  }

  function render() {
    list.innerHTML = "";
    (state.profiles || []).forEach(function (p) {
      ensureProfileShapes(p);
      const li = document.createElement("li");
      li.textContent = p.name + (p.baseFolder ? " — " + p.baseFolder : "");
      if (p.name === state.selectedProfile) li.className = "active";
      li.addEventListener("click", async function () {
        readFormIntoState();
        state.selectedProfile = p.name;
        fillForm();
        render();
        await HostApi.call("host.config.set", {
          config: JSON.stringify(Object.assign({}, state, { profiles: profilesForBridge() }))
        });
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
    readFormIntoState();
    Object.assign(state, extra || {});
    const payload = Object.assign({}, state, { profiles: profilesForBridge() });
    await HostApi.call("host.config.set", { config: JSON.stringify(payload) });
  }

  document.querySelectorAll(".tab").forEach(function (btn) {
    btn.addEventListener("click", function () {
      readFormIntoState();
      document.querySelectorAll(".tab").forEach(function (b) {
        b.classList.toggle("active", b === btn);
      });
      const tab = btn.getAttribute("data-tab");
      document.getElementById("panel-overview").classList.toggle("hidden", tab !== "overview");
      document.getElementById("panel-options").classList.toggle("hidden", tab !== "options");
      document.getElementById("panel-empty").classList.toggle("hidden", tab !== "empty");
      if (tab === "empty") fillEmptyForm();
    });
  });

  document.getElementById("emptyField").addEventListener("change", function () {
    const p = selectedProfile();
    if (!p) return;
    ensureProfileShapes(p);
    if (lastEmptyField) {
      p.emptyData[lastEmptyField] = document.getElementById("emptyValue").value || "";
    }
    const field = document.getElementById("emptyField").value;
    document.getElementById("emptyValue").value = p.emptyData[field] || "";
    lastEmptyField = field;
  });

  document.getElementById("emptyValue").addEventListener("input", function () {
    const p = selectedProfile();
    if (!p) return;
    ensureProfileShapes(p);
    const field = document.getElementById("emptyField").value;
    p.emptyData[field] = document.getElementById("emptyValue").value || "";
  });

  document.getElementById("btnAddExcluded").addEventListener("click", function () {
    const p = selectedProfile();
    if (!p) return;
    ensureProfileShapes(p);
    const path = (document.getElementById("excludedPath").value || "").trim();
    if (!path) return;
    if (p.excludedEmptyFolder.indexOf(path) < 0) p.excludedEmptyFolder.push(path);
    document.getElementById("excludedPath").value = "";
    renderExcludedList();
  });

  try {
    const info = await HostApi.call("host.getInfo");
    hostMeta.textContent =
      "Host " + info.productVersion + " · API v" + info.apiVersion + " · SPA Configure Phase D";

    const cfg = await HostApi.call("host.config.get");
    if (cfg && cfg.config) {
      try {
        state = Object.assign(state, JSON.parse(cfg.config));
        (state.profiles || []).forEach(ensureProfileShapes);
      } catch (e) {
        hostMeta.textContent += " (bridge parse warning)";
      }
    }
    if (!state.selectedProfile && state.lastUsed) state.selectedProfile = state.lastUsed;
    if (!state.selectedProfile && state.profiles && state.profiles[0]) {
      state.selectedProfile = state.profiles[0].name;
    }
    fillEmptyFieldSelect();
    render();
    fillForm();
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
