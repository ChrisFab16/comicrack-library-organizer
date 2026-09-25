"""
libraryorganizer.py

The entry area for ComicRack

Version 2.0

Copyright 2010-2012 Stonepaw

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import clr
import System

import System.IO
from System.IO import File, StreamReader, StreamWriter

clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import (
    Application, DialogResult, Form, FormBorderStyle, FormStartPosition,
    Label, MessageBox, MessageBoxButtons, MessageBoxIcon, ProgressBar,
    ProgressBarStyle
)
from System.Drawing import Size, Font, FontStyle, SystemFonts, ContentAlignment


clr.AddReference("System.Xml")
import System.Xml
from System.Xml import XmlWriter, Formatting, XmlTextWriter, XmlWriterSettings, XmlDocument

import configureform
from configureform import ConfigureForm

import losettings
from losettings import load_profiles, save_profiles, save_last_used

import loworkerform
from loworkerform import ProfileSelector, WorkerForm, WorkerFormUndo

import locommon
from locommon import PROFILEFILE, UNDOFILE, UndoCollection, SCRIPTDIRECTORY, Mode

import lobookmover


#@Name Library Organizer
#@Hook Books
#@Key library-organizer-main
#@Image libraryorganizer.png
def LibraryOrganizer(books):
    if books:
        try:
            profiles, lastused = load_profiles(PROFILEFILE)

            loworkerform.ComicRack = ComicRack
            locommon.ComicRack = ComicRack
            lobookmover.ComicRack = ComicRack
            #Create the config form
            print "Creating config form"
            if show_config_form(profiles, lastused, books):
                show_worker_form(profiles, lastused, books)

        except Exception, ex:
            print "The following error occured"
            print Exception
            MessageBox.Show(str(ex))


#@Name Configure Library Organizer
#@Hook Library
#@Image libraryorganizer.png
def ConfigureLibraryOrganizer(books, wait=None):
    try:
        locommon.ComicRack = ComicRack
        lobookmover.ComicRack = ComicRack
        profiles, lastused = load_profiles(PROFILEFILE)
        if books is None:
            # Library hook: load books for preview. ConfigScript fallback passes [].
            _set_wait_message(wait, "Loading library books…")
            books = ComicRack.App.GetLibraryBooks()
        show_config_form(profiles, lastused, books, wait)
        
    except Exception, ex:
        _close_wait_form(wait)
        print "The Following error occured"
        print Exception
        MessageBox.Show(str(ex))


#@Key library-organizer-main
#@Hook ConfigScript
def ConfigLibraryOrganizer():
    wait = _show_wait_form("Opening Configure…")
    try:
        if _try_spa_configure(wait):
            wait = None  # closed inside before ShowWebConfigure
            return
        _set_wait_message(wait, "Loading classic Configure…")
        # Do not call GetLibraryBooks here — large libraries make classic Configure look hung.
        ConfigureLibraryOrganizer([], wait)
        wait = None  # closed inside show_config_form before ShowDialog
    finally:
        _close_wait_form(wait)


def _show_wait_form(message):
    """Top-most wait banner so Configure never appears to do nothing."""
    try:
        f = Form()
        f.Text = "Library Organizer"
        f.FormBorderStyle = FormBorderStyle.FixedDialog
        f.ControlBox = False
        f.ShowInTaskbar = False
        f.StartPosition = FormStartPosition.CenterScreen
        f.TopMost = True
        f.MinimizeBox = False
        f.MaximizeBox = False
        f.Size = Size(400, 120)
        lbl = Label()
        lbl.Text = message
        lbl.Dock = System.Windows.Forms.DockStyle.Fill
        lbl.TextAlign = ContentAlignment.MiddleCenter
        try:
            lbl.Font = Font(SystemFonts.MessageBoxFont.FontFamily, 10, FontStyle.Regular)
        except Exception:
            pass
        bar = ProgressBar()
        bar.Style = ProgressBarStyle.Marquee
        bar.MarqueeAnimationSpeed = 30
        bar.Dock = System.Windows.Forms.DockStyle.Bottom
        bar.Height = 22
        f.Controls.Add(lbl)
        f.Controls.Add(bar)
        f.Show()
        Application.DoEvents()
        return f
    except Exception:
        return None


def _close_wait_form(f):
    if f is None:
        return
    try:
        f.Close()
        f.Dispose()
    except Exception:
        pass
    try:
        Application.DoEvents()
    except Exception:
        pass


def _set_wait_message(f, message):
    if f is None:
        return
    try:
        for c in f.Controls:
            if isinstance(c, Label):
                c.Text = message
                break
        Application.DoEvents()
    except Exception:
        pass


def _can_show_web_configure():
    """True when CE Host API is present and SPA Configure is not forced off.

    Place an empty file named force-classic-configure next to this script to skip
    WebView2 Configure (use when SPA hang/lock is suspected).
    """
    if not hasattr(ComicRack, "ShowWebConfigure"):
        return False
    try:
        sentinel = System.IO.Path.Combine(SCRIPTDIRECTORY, "force-classic-configure")
        if File.Exists(sentinel):
            return False
    except Exception:
        pass
    return True


def _bridge_path():
    return System.IO.Path.Combine(SCRIPTDIRECTORY, "webview-ui.config")


def _json_esc(s):
    if s is None:
        return ""
    return str(s).replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "")


def _json_bool(v):
    return "true" if v else "false"


def _json_string_list(items):
    """Serialize a sequence of strings as a JSON array."""
    parts = []
    if items:
        for item in items:
            parts.append("\"%s\"" % _json_esc(item))
    return "[%s]" % ",".join(parts)


def _json_empty_data(empty_data):
    """Serialize EmptyData dict as [{field,value}, ...]."""
    parts = []
    if empty_data:
        for key in empty_data.keys():
            val = empty_data[key]
            if val is None:
                val = ""
            parts.append(
                "{\"field\":\"%s\",\"value\":\"%s\"}"
                % (_json_esc(str(key)), _json_esc(str(val)))
            )
    return "[%s]" % ",".join(parts)


def _profile_overview_item(name, p):
    mode = Mode.Move
    try:
        mode = p.Mode or Mode.Move
    except Exception:
        pass
    base = ""
    try:
        base = p.BaseFolder or ""
    except Exception:
        pass
    empty_folder = ""
    try:
        empty_folder = p.EmptyFolder or ""
    except Exception:
        pass
    fileless = ".jpg"
    try:
        fileless = p.FilelessFormat or ".jpg"
    except Exception:
        pass
    failed = ""
    try:
        failed = p.FailedFolder or ""
    except Exception:
        pass
    empty_data = {}
    try:
        empty_data = getattr(p, "EmptyData", None) or {}
    except Exception:
        empty_data = {}
    failed_fields = []
    try:
        failed_fields = list(getattr(p, "FailedFields", None) or [])
    except Exception:
        failed_fields = []
    excluded_empty = []
    try:
        excluded_empty = list(getattr(p, "ExcludedEmptyFolder", None) or [])
    except Exception:
        excluded_empty = []
    return (
        "{\"name\":\"%s\",\"baseFolder\":\"%s\",\"mode\":\"%s\","
        "\"useFolder\":%s,\"useFileName\":%s,\"copyMode\":%s,\"moveFileless\":%s,"
        "\"dontAskWhenMultiOne\":%s,\"removeEmptyFolder\":%s,"
        "\"emptyFolder\":\"%s\",\"filelessFormat\":\"%s\","
        "\"failEmptyValues\":%s,\"moveFailed\":%s,\"failedFolder\":\"%s\","
        "\"emptyData\":%s,\"failedFields\":%s,\"excludedEmptyFolder\":%s}"
    ) % (
        _json_esc(name),
        _json_esc(base),
        _json_esc(mode),
        _json_bool(bool(getattr(p, "UseFolder", True))),
        _json_bool(bool(getattr(p, "UseFileName", True))),
        _json_bool(bool(getattr(p, "CopyMode", True))),
        _json_bool(bool(getattr(p, "MoveFileless", False))),
        _json_bool(bool(getattr(p, "DontAskWhenMultiOne", True))),
        _json_bool(bool(getattr(p, "RemoveEmptyFolder", True))),
        _json_esc(empty_folder),
        _json_esc(fileless),
        _json_bool(bool(getattr(p, "FailEmptyValues", False))),
        _json_bool(bool(getattr(p, "MoveFailed", False))),
        _json_esc(failed),
        _json_empty_data(empty_data),
        _json_string_list(failed_fields),
        _json_string_list(excluded_empty),
    )


def _write_spa_bridge(profiles, lastused):
    """Serialize profile Overview + Options + Empty values for the Configure SPA (Phase D)."""
    parts = []
    for name in profiles.keys():
        parts.append(_profile_overview_item(name, profiles[name]))
    last_name = ""
    if lastused:
        try:
            last_name = lastused[0] if hasattr(lastused, "__getitem__") else lastused
        except Exception:
            last_name = str(lastused)
    selected = _json_esc(last_name) if last_name else (_json_esc(profiles.keys()[0]) if len(profiles) else "")
    body = (
        "{\"version\":\"2.2.6\",\"lastUsed\":\"%s\",\"selectedProfile\":\"%s\","
        "\"openClassic\":false,\"saveOverview\":false,\"profiles\":[%s]}"
    ) % (_json_esc(last_name), selected, ",".join(parts))
    File.WriteAllText(_bridge_path(), body)


def _bridge_extract_string(text, key):
    marker = "\"%s\":\"" % key
    idx = text.find(marker)
    if idx < 0:
        return None
    start = idx + len(marker)
    end = start
    while end < len(text):
        if text[end] == "\\" and end + 1 < len(text):
            end += 2
            continue
        if text[end] == "\"":
            break
        end += 1
    if end > start:
        return text[start:end].replace("\\\"", "\"").replace("\\\\", "\\")
    return None


def _bridge_extract_bool(text, key):
    compact = text.replace(" ", "")
    if "\"%s\":true" % key in compact:
        return True
    if "\"%s\":false" % key in compact:
        return False
    return None


def _bridge_array_body(text, key):
    """Return the inner text of a JSON array value for key, or None if missing."""
    marker = "\"%s\":[" % key
    idx = text.find(marker)
    if idx < 0:
        return None
    start = idx + len(marker)
    depth = 1
    end = start
    while end < len(text) and depth > 0:
        ch = text[end]
        if ch == "\\" and end + 1 < len(text):
            end += 2
            continue
        if ch == "\"":
            end += 1
            while end < len(text):
                if text[end] == "\\" and end + 1 < len(text):
                    end += 2
                    continue
                if text[end] == "\"":
                    end += 1
                    break
                end += 1
            continue
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return text[start:end]
        end += 1
    return None


def _bridge_extract_string_list(text, key):
    """Parse a JSON string array. Returns None if key absent, else a list (possibly empty)."""
    body = _bridge_array_body(text, key)
    if body is None:
        return None
    items = []
    i = 0
    n = len(body)
    while i < n:
        if body[i] != "\"":
            i += 1
            continue
        i += 1
        start = i
        while i < n:
            if body[i] == "\\" and i + 1 < n:
                i += 2
                continue
            if body[i] == "\"":
                break
            i += 1
        raw = body[start:i]
        items.append(raw.replace("\\\"", "\"").replace("\\\\", "\\"))
        i += 1
    return items


def _bridge_extract_empty_data(text):
    """Parse emptyData array of {field,value} into a dict. None if key absent."""
    body = _bridge_array_body(text, "emptyData")
    if body is None:
        return None
    result = {}
    # Walk objects in the array
    search_from = 0
    while True:
        fidx = body.find("\"field\":\"", search_from)
        if fidx < 0:
            break
        field = _bridge_extract_string(body[fidx:], "field")
        value = _bridge_extract_string(body[fidx:], "value")
        if field is not None:
            result[field] = value if value is not None else ""
        search_from = fidx + 8
    return result


def _bridge_profile_chunk(text, name):
    """Return the full JSON object text for a profile by name (brace-matched).

    Must not slice on the first ']' — Phase D arrays (emptyData, etc.) contain
    brackets inside the profile object.
    """
    marker = "\"name\":\"%s\"" % _json_esc(name)
    idx = text.find(marker)
    if idx < 0:
        return None
    start = idx
    while start > 0 and text[start] != "{":
        start -= 1
    if text[start] != "{":
        return None
    depth = 0
    end = start
    while end < len(text):
        ch = text[end]
        if ch == "\\" and end + 1 < len(text):
            end += 2
            continue
        if ch == "\"":
            end += 1
            while end < len(text):
                if text[end] == "\\" and end + 1 < len(text):
                    end += 2
                    continue
                if text[end] == "\"":
                    end += 1
                    break
                end += 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start : end + 1]
        end += 1
    return None


def _read_spa_bridge():
    path = _bridge_path()
    if not File.Exists(path):
        return None
    try:
        text = File.ReadAllText(path)
        return {
            "openClassic": _bridge_extract_bool(text, "openClassic") is True,
            "saveOverview": _bridge_extract_bool(text, "saveOverview") is True,
            "selectedProfile": _bridge_extract_string(text, "selectedProfile"),
            "raw": text,
        }
    except Exception:
        return None


def _apply_overview_from_bridge(profiles, bridge):
    """Apply SPA overview edits to Profile objects. Returns True if saved."""
    if not bridge or not bridge.get("saveOverview"):
        return False
    text = bridge.get("raw") or ""
    # Walk each known profile and patch fields from the JSON blob by name.
    for name in list(profiles.keys()):
        chunk = _bridge_profile_chunk(text, name)
        if not chunk:
            continue
        p = profiles[name]
        base = _bridge_extract_string(chunk, "baseFolder")
        if base is not None:
            p.BaseFolder = base
        mode = _bridge_extract_string(chunk, "mode")
        if mode in (Mode.Move, Mode.Copy, Mode.Simulate):
            p.Mode = mode
        uf = _bridge_extract_bool(chunk, "useFolder")
        if uf is not None:
            p.UseFolder = uf
        un = _bridge_extract_bool(chunk, "useFileName")
        if un is not None:
            p.UseFileName = un
        cm = _bridge_extract_bool(chunk, "copyMode")
        if cm is not None:
            p.CopyMode = cm
        mf = _bridge_extract_bool(chunk, "moveFileless")
        if mf is not None:
            p.MoveFileless = mf
        da = _bridge_extract_bool(chunk, "dontAskWhenMultiOne")
        if da is not None:
            p.DontAskWhenMultiOne = da
        re = _bridge_extract_bool(chunk, "removeEmptyFolder")
        if re is not None:
            p.RemoveEmptyFolder = re
        ef = _bridge_extract_string(chunk, "emptyFolder")
        if ef is not None:
            p.EmptyFolder = ef
        ff = _bridge_extract_string(chunk, "filelessFormat")
        if ff is not None:
            p.FilelessFormat = ff
        fe = _bridge_extract_bool(chunk, "failEmptyValues")
        if fe is not None:
            p.FailEmptyValues = fe
        mv = _bridge_extract_bool(chunk, "moveFailed")
        if mv is not None:
            p.MoveFailed = mv
        fd = _bridge_extract_string(chunk, "failedFolder")
        if fd is not None:
            p.FailedFolder = fd
        empty_data = _bridge_extract_empty_data(chunk)
        if empty_data is not None:
            p.EmptyData = empty_data
        failed_fields = _bridge_extract_string_list(chunk, "failedFields")
        if failed_fields is not None:
            p.FailedFields = failed_fields
        excluded = _bridge_extract_string_list(chunk, "excludedEmptyFolder")
        if excluded is not None:
            p.ExcludedEmptyFolder = excluded

    selected = bridge.get("selectedProfile")
    lastused = [selected] if selected else [profiles.keys()[0]]
    save_profiles(PROFILEFILE, profiles, lastused)
    try:
        save_last_used(PROFILEFILE, lastused)
    except Exception:
        pass
    return True


def _try_spa_configure(wait=None):
    """Open WebView2 SPA Configure when CE Host API is available. Returns True if handled."""
    if not _can_show_web_configure():
        return False
    try:
        locommon.ComicRack = ComicRack
        lobookmover.ComicRack = ComicRack
        _set_wait_message(wait, "Preparing Configure…")
        profiles, lastused = load_profiles(PROFILEFILE)
        _write_spa_bridge(profiles, lastused)
        # Close wait before modal SPA so it does not cover the Configure dialog.
        _close_wait_form(wait)
        wait = None
        ComicRack.ShowWebConfigure(SCRIPTDIRECTORY)
        bridge = _read_spa_bridge()
        if bridge and bridge.get("openClassic"):
            books = []
            show_config_form(profiles, lastused, books, None)
        else:
            _apply_overview_from_bridge(profiles, bridge)
            if bridge and bridge.get("selectedProfile") and not bridge.get("saveOverview"):
                try:
                    save_last_used(PROFILEFILE, [bridge["selectedProfile"]])
                except Exception:
                    pass
        return True
    except Exception, ex:
        print "SPA Configure failed; falling back to WinForms"
        print ex
        MessageBox.Show("SPA Configure failed (%s). Opening classic Configure." % str(ex))
        return False


#@Name Library Organizer (Quick)
#@Hook Books
#@Key library-organizer-quick
#@Image libraryorganizerquick.png
def LibraryOrganizerQuick(books):
    if books:
        try:
            loworkerform.ComicRack = ComicRack
            locommon.ComicRack = ComicRack
            lobookmover.ComicRack = ComicRack
            profiles, lastused = load_profiles(PROFILEFILE)

            if len(profiles) == 1 and profiles[profiles.keys()[0]].BaseFolder == "":
                MessageBox.Show("Library Organizer will not work as expected when the BaseFolder is empty. Please run the normal Library Organizer script or the Configure Library Organizer script before running Library Organizer Quick", "BaseFolder empty", MessageBoxButtons.OK, MessageBoxIcon.Warning)
                return
            
            show_worker_form(profiles, lastused, books)

        except Exception, ex:
            print "The following error occured"
            print Exception
            MessageBox.Show(str(ex))
      
              
#@Name Library Organizer - Undo last move
#@Hook Library
#@Image libraryorganizer.png
def LibraryOrganizerUndo(books):
    try:
        if File.Exists(UNDOFILE):
            loworkerform.ComicRack = ComicRack
            locommon.ComicRack = ComicRack
            lobookmover.ComicRack = ComicRack
            profiles, lastused = load_profiles(PROFILEFILE)
                
            undo_collection = UndoCollection()

            undo_collection.load(UNDOFILE)

            if len(undo_collection) > 0:
                undo_form = WorkerFormUndo(undo_collection, profiles)
                undo_form.ShowDialog()
                undo_form.Dispose()
                File.Delete(UNDOFILE)
            else:
                MessageBox.Show("Error loading Undo file", "Library Organizer - Undo")
        else:
            MessageBox.Show("Nothing to Undo", "Library Organizer - Undo")
    except Exception, ex:
        print "The following error occured"
        print Exception
        MessageBox.Show(str(ex))


#@Name Library Organizer - Startup
#@Enabled false
#@Hook Startup
#@Image libraryorganizer.png
def LibraryOrganizerStartup():
    books = ComicRack.App.GetLibraryBooks()
    LibraryOrganizerQuick(books)


def show_config_form(profiles, lastused, books, wait=None):
    """Shows the configure form and saves the changes if the user press okay.
    Returns True if the user press Okay.
    Returns False if the user pressed cancel."""
    _set_wait_message(wait, "Building Configure window…")
    configform = ConfigureForm(profiles, lastused[0], books)
    _close_wait_form(wait)
    result = configform.ShowDialog()
    configform.save_profile()
    configform.Dispose()
    if result != DialogResult.Cancel:
        save_profiles(PROFILEFILE, profiles, lastused)
        return True
    return False


def show_worker_form(profiles, lastused, books):
    """Gets the profile(s) to use and shows the worker form."""
    if len(profiles) > 1:
        profile_selector = ProfileSelector(profiles.keys(), lastused)
        result = profile_selector.ShowDialog()
        if result == DialogResult.Cancel:
            profile_selector.Dispose()
            return
        lastused = profile_selector.get_profiles_to_use()
        save_last_used(PROFILEFILE, lastused)
        profile_selector.Dispose()

    profiles_to_use = [profiles[name] for name in lastused]

    worker_form = WorkerForm(books, profiles_to_use)
    worker_form.ShowDialog()