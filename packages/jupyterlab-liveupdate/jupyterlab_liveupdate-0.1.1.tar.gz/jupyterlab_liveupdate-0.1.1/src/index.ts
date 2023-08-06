import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IDocumentManager } from '@jupyterlab/docmanager';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { updateWatchedFiles } from './updater';
import { ICommandPalette } from '@jupyterlab/apputils';

const UPDATER_PLUGIN_NAME = 'jupyterlab-liveupdate:liveupdater';
// import { requestAPI } from './handler';

/**
 * Initialization data for the jupyterlab-liveupdate extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-liveupdate:plugin',
  autoStart: true,
  requires: [IDocumentManager, ISettingRegistry, ICommandPalette],
  activate: async (
    app: JupyterFrontEnd,
    docManager: IDocumentManager,
    settingRegistry: ISettingRegistry,
    palette: ICommandPalette
  ) => {
    // Define the file paths to watch
    let watchedFiles: string[] = [];
    const cm = docManager.services.contents;
    updateWatchedFiles(
      cm,
      (await settingRegistry.get(UPDATER_PLUGIN_NAME, 'watchedFilesPatterns'))
        .composite as string[],
      (await settingRegistry.get(UPDATER_PLUGIN_NAME, 'watchedSpecificDirs'))
        .composite as string[],
      (await settingRegistry.get(UPDATER_PLUGIN_NAME, 'excludedDirs'))
        .composite as string[],
      (await settingRegistry.get(UPDATER_PLUGIN_NAME, 'excludedFiles'))
        .composite as string[]
    ).then((files: string[]) => {
      watchedFiles = files;
    });

    settingRegistry.pluginChanged.connect(async (sender, plugin) => {
      if (plugin === UPDATER_PLUGIN_NAME) {
        watchedFiles = await updateWatchedFiles(
          cm,
          (
            await sender.get(plugin, 'watchedFilesPatterns')
          ).composite as string[],
          (
            await sender.get(plugin, 'watchedSpecificDirs')
          ).composite as string[],
          (
            await sender.get(plugin, 'excludedDirs')
          ).composite as string[],
          (
            await sender.get(plugin, 'excludedFiles')
          ).composite as string[]
        );
      }
    });

    // Start the interval for watching the files
    setInterval(() => {
      const now = Date.now();
      for (const file of watchedFiles) {
        cm.get(file).then(model => {
          const last_modif = Date.parse(model.last_modified);
          if (last_modif >= now - 1000) {
            console.log('Evaluating content of file ' + model.name);
            eval(model.content);
          }
        });
      }
    }, 1000);
  }
};

export default plugin;
