const { getDefaultConfig, mergeConfig } = require("@react-native/metro-config");
const path = require("path");

// El monorepo vive dos niveles arriba (TV app/). Metro necesita ver el núcleo
// compartido (@tvapp/core) y su node_modules para resolverlo.
const workspaceRoot = path.resolve(__dirname, "../..");
const projectRoot = __dirname;

const config = {
  watchFolders: [workspaceRoot],
  resolver: {
    nodeModulesPaths: [
      path.resolve(projectRoot, "node_modules"),
      path.resolve(workspaceRoot, "node_modules"),
    ],
  },
};

module.exports = mergeConfig(getDefaultConfig(projectRoot), config);
