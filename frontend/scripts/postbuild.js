const fs = require("fs");
const path = require("path");

// Frontend urls
const FRONTEND_BUILD_FOLDER = path.join(__dirname, "..", "build");
const FRONTEND_STATIC_FOLDER = path.join(FRONTEND_BUILD_FOLDER, "static");
const FRONTEND_INDEX_FILE = path.join(FRONTEND_BUILD_FOLDER, "index.html");

// Backend urls
const BACKEND_STATIC_FOLDER = path.join(__dirname, "..", "..", "backend", "react", "static");
if (!fs.existsSync(BACKEND_STATIC_FOLDER)) fs.mkdirSync(BACKEND_STATIC_FOLDER);

const BACKEND_TEMPLATE_FOLDER = path.join(__dirname, "..", "..", "backend", "react", "templates");
if (!fs.existsSync(BACKEND_TEMPLATE_FOLDER)) fs.mkdirSync(BACKEND_TEMPLATE_FOLDER);

const BACKEND_TEMPLATE_INDEX_FILE = path.join(BACKEND_TEMPLATE_FOLDER, "index.html");

function log(message) {
    console.log(`[POSTBUILD] ${message}`);
}

// Clear the backend static folder prior to copying new files
function clearStaticFolder() {
    log("Clearing old static files...");

    const entries = fs.readdirSync(BACKEND_STATIC_FOLDER);
    for (const entry of entries) {
        const clearedEntryPath = path.join(BACKEND_STATIC_FOLDER, entry);

        // Delete recursively + forcefully
        fs.rmSync(clearedEntryPath, { recursive: true });
        log(`[REMOVING] Removed ${clearedEntryPath}`);
    }

    log("Cleared all old static files!");
}

// The index.html file is special in that it's a template rather than a static file 
// (this is done so that we can get rid of the /static/ prefix as a template)
function copyReactIndexFile() {
    log("Copying react index file...");
    fs.copyFileSync(FRONTEND_INDEX_FILE, BACKEND_TEMPLATE_INDEX_FILE);
    log("Copied react index file!");
}

// Copy over the remainin static files (that are not index.html) to the static folder
function copyReactStaticFiles(staticDirRelativePath = "") {
    const entries = fs.readdirSync(path.join(FRONTEND_STATIC_FOLDER, staticDirRelativePath));

    for (const entry of entries) {
        if (entry === "index.html") {
            continue;   // index.html is handled differently from other files
        }

        // Where is it and where does it need to go?
        const entryPath = path.join(FRONTEND_STATIC_FOLDER, staticDirRelativePath, entry);
        const targetPath = path.join(BACKEND_STATIC_FOLDER, staticDirRelativePath, entry);

        const isDir = fs.lstatSync(entryPath).isDirectory();
        if (isDir) {
            // It's a directory, so we need to mkdir it and then recurisvely go through it.
            fs.mkdirSync(targetPath);
            log(`[COPYING] Copied ${path.join(staticDirRelativePath, entry)}`);

            copyReactStaticFiles(path.join(staticDirRelativePath, entry));
        } else {
            // It's just a file so we can just copy it.
            fs.copyFileSync(entryPath, targetPath);
            log(`[COPYING] Copied ${path.join(staticDirRelativePath, entry)}`);
        }
    }
}

// Clear static folder first
clearStaticFolder();

// Copy the index.html file
copyReactIndexFile();

// Copy over the remaining static files
log("Copying non-template react build files...");
copyReactStaticFiles();
log("Copied non-template react files!");

// Huzzah oWo
log("Success!");