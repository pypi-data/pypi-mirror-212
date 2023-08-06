import { Contents } from '@jupyterlab/services';

export async function updateWatchedFiles(
  cm: Contents.IManager,
  regExList: string[],
  lookupFolders: string[],
  excludedFolders: string[],
  excludedFiles: string[]
): Promise<string[]> {
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
  let watchedFiles: string[] = [];
  for (const folder of lookupFolders) {
    watchedFiles = watchedFiles.concat(
      await searchFolder(cm, folder, regExes, excludedFiles, excludedFolders)
    );
  }

  if (lookupFolders.length === 0) {
    const root = await cm.get('');
    watchedFiles = watchedFiles.concat(
      await searchFolder(cm, root.path, regExes, excludedFiles, excludedFolders)
    );
  }
  return watchedFiles;
}

function patternToRegex(pattern: string): RegExp {
  const regex =
    '^' +
    pattern
      .replace(/([.?+^$[\]\\(){}|-])/g, '\\$1')
      .replace(/\*/g, '.*')
      .replace(/\\\*/g, '\\*') +
    '$';
  return new RegExp(regex);
}

async function searchFolder(
  cm: Contents.IManager,
  path: string,
  regExes: RegExp[],
  excludedFiles: string[],
  excludedFolders: string[]
): Promise<string[]> {
  const folderContents = await cm.get(path);
  let watchedFiles: string[] = [];
  for (const file of folderContents.content) {
    // dig more if the file is not an excluded folder
    if (file.type === 'directory') {
      if (
        !excludedFolders.some(excludedFolder =>
          file.path.startsWith(excludedFolder)
        )
      ) {
        watchedFiles = watchedFiles.concat(
          await searchFolder(
            cm,
            file.path,
            regExes,
            excludedFiles,
            excludedFolders
          )
        );
      }
      continue;
    }
    // add the file if it matches the regex and is not an excluded file
    if (
      regExes.some(regEx => regEx.test(file.path)) &&
      !excludedFiles.some(excludedFile => file.path === excludedFile)
    ) {
      watchedFiles.push(file.path);
    }
  }
  return watchedFiles;
}
