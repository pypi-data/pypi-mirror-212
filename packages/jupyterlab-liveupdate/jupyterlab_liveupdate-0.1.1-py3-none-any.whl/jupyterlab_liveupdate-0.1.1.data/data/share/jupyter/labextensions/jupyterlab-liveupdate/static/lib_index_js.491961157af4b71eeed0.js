"use strict";
(self["webpackChunkjupyterlab_liveupdate"] = self["webpackChunkjupyterlab_liveupdate"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _updater__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./updater */ "./lib/updater.js");



const UPDATER_PLUGIN_NAME = 'jupyterlab-liveupdate:liveupdater';
// import { requestAPI } from './handler';
/**
 * Initialization data for the jupyterlab-liveupdate extension.
 */
const plugin = {
    id: 'jupyterlab-liveupdate:plugin',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_0__.IDocumentManager, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry],
    activate: async (app, docManager, settingRegistry) => {
        // Define the file paths to watch
        let watchedFiles = [];
        const cm = docManager.services.contents;
        (0,_updater__WEBPACK_IMPORTED_MODULE_2__.updateWatchedFiles)(cm, (await settingRegistry.get(UPDATER_PLUGIN_NAME, 'watchedFilesPatterns'))
            .composite, (await settingRegistry.get(UPDATER_PLUGIN_NAME, 'watchedSpecificDirs'))
            .composite, (await settingRegistry.get(UPDATER_PLUGIN_NAME, 'excludedDirs'))
            .composite, (await settingRegistry.get(UPDATER_PLUGIN_NAME, 'excludedFiles'))
            .composite).then((files) => {
            watchedFiles = files;
        });
        settingRegistry.pluginChanged.connect(async (sender, plugin) => {
            if (plugin === UPDATER_PLUGIN_NAME) {
                watchedFiles = await (0,_updater__WEBPACK_IMPORTED_MODULE_2__.updateWatchedFiles)(cm, (await sender.get(plugin, 'watchedFilesPatterns')).composite, (await sender.get(plugin, 'watchedSpecificDirs')).composite, (await sender.get(plugin, 'excludedDirs')).composite, (await sender.get(plugin, 'excludedFiles')).composite);
            }
        });
        // Start the interval for watching the files
        setInterval(() => {
            const now = Date.now();
            for (const file of watchedFiles) {
                cm.get(file).then(model => {
                    const last_modif = Date.parse(model.last_modified);
                    if (last_modif >= now - 1000) {
                        eval(model.content);
                    }
                });
            }
        }, 1000);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/updater.js":
/*!************************!*\
  !*** ./lib/updater.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "updateWatchedFiles": () => (/* binding */ updateWatchedFiles)
/* harmony export */ });
async function updateWatchedFiles(cm, regExList, lookupFolders, excludedFolders, excludedFiles) {
    if (regExList === undefined) {
        regExList = [];
    }
    if (lookupFolders === undefined) {
        lookupFolders = [];
    }
    if (excludedFolders === undefined) {
        excludedFolders = [];
    }
    if (excludedFiles === undefined) {
        excludedFiles = [];
    }
    const regExes = regExList.map(regEx => patternToRegex(regEx));
    let watchedFiles = [];
    for (const folder of lookupFolders) {
        watchedFiles = watchedFiles.concat(await searchFolder(cm, folder, regExes, excludedFiles, excludedFolders));
    }
    if (lookupFolders.length === 0) {
        const root = await cm.get('');
        watchedFiles = watchedFiles.concat(await searchFolder(cm, root.path, regExes, excludedFiles, excludedFolders));
    }
    return watchedFiles;
}
function patternToRegex(pattern) {
    const regex = '^' +
        pattern
            .replace(/([.?+^$[\]\\(){}|-])/g, '\\$1')
            .replace(/\*/g, '.*')
            .replace(/\\\*/g, '\\*') +
        '$';
    return new RegExp(regex);
}
async function searchFolder(cm, path, regExes, excludedFiles, excludedFolders) {
    const folderContents = await cm.get(path);
    let watchedFiles = [];
    for (const file of folderContents.content) {
        // dig more if the file is not an excluded folder
        if (file.type === 'directory') {
            if (!excludedFolders.some(excludedFolder => file.path.startsWith(excludedFolder))) {
                watchedFiles = watchedFiles.concat(await searchFolder(cm, file.path, regExes, excludedFiles, excludedFolders));
            }
            continue;
        }
        // add the file if it matches the regex and is not an excluded file
        if (regExes.some(regEx => regEx.test(file.path)) &&
            !excludedFiles.some(excludedFile => file.path === excludedFile)) {
            watchedFiles.push(file.path);
        }
    }
    return watchedFiles;
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.491961157af4b71eeed0.js.map