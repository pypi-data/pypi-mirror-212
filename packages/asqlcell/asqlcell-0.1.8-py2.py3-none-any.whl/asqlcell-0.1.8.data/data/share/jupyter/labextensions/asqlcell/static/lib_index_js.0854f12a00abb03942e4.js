"use strict";
(self["webpackChunkasqlcell"] = self["webpackChunkasqlcell"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
__exportStar(__webpack_require__(/*! ./version */ "./lib/version.js"), exports);
__exportStar(__webpack_require__(/*! ./WidgetModel */ "./lib/WidgetModel.js"), exports);
__exportStar(__webpack_require__(/*! ./table/table */ "./lib/table/table.js"), exports);
__exportStar(__webpack_require__(/*! ./input/dataimport */ "./lib/input/dataimport.js"), exports);
//# sourceMappingURL=index.js.map

/***/ }),

/***/ "./lib/input/dataimport.js":
/*!*********************************!*\
  !*** ./lib/input/dataimport.js ***!
  \*********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.DataImport = void 0;
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const ri_1 = __webpack_require__(/*! react-icons/ri */ "./node_modules/react-icons/ri/index.esm.js");
const hooks_1 = __webpack_require__(/*! ../hooks */ "./lib/hooks.js");
const DataImport = () => {
    const model = hooks_1.useModel();
    const [opened, setOpened] = react_1.useState(false);
    const [dataframe, setDataFrame] = react_1.useState(model === null || model === void 0 ? void 0 : model.get("dfs_result"));
    model === null || model === void 0 ? void 0 : model.on("change:dfs_result", (msg) => {
        setDataFrame(model.get("dfs_result"));
    });
    const DropdownHeight = dataframe.trim().split(/\r?\n/).length >= 5 ? "125px" : `${dataframe.trim().split(/\r?\n/).length * 25}px`;
    const items = dataframe.split("\n").map((name, index) => (name === "" ?
        react_1.default.createElement(react_1.default.Fragment, null)
        :
            react_1.default.createElement(core_1.NavLink, { sx: { height: "25px" }, className: "data list", key: index, label: name.split("\t")[0], onClick: () => {
                    model === null || model === void 0 ? void 0 : model.trigger("importData", name.split("\t")[0]);
                    setOpened(false);
                }, rightSection: react_1.default.createElement(core_1.Text, { size: "xs" }, name.split("\t")[1]) })));
    return (react_1.default.createElement(react_1.default.Fragment, null,
        react_1.default.createElement(core_1.Popover, { opened: opened, onChange: setOpened },
            react_1.default.createElement(core_1.Popover.Target, null,
                react_1.default.createElement(core_1.Button, { rightIcon: react_1.default.createElement(ri_1.RiArrowDownSLine, null), color: "dark", variant: "subtle", radius: "xs", sx: {
                        outline: "none",
                        "&:hover": {
                            backgroundColor: "transparent"
                        },
                    }, onClick: () => {
                        setOpened((open) => !open);
                        model === null || model === void 0 ? void 0 : model.trigger("dfs_button");
                    } },
                    react_1.default.createElement(core_1.Text, { color: "gray", sx: { fontWeight: "bold" } }, "Dataframe"))),
            react_1.default.createElement(core_1.Popover.Dropdown, { sx: {
                    marginLeft: "2.5%",
                    marginTop: "-15px",
                    padding: "2px",
                } }, dataframe ?
                react_1.default.createElement(core_1.ScrollArea, { sx: { height: DropdownHeight } },
                    react_1.default.createElement(core_1.Group, { style: { width: "100%" } },
                        react_1.default.createElement(core_1.Box, { sx: {
                                padding: 0,
                            } }, items)))
                :
                    react_1.default.createElement(core_1.Text, { color: "lightgray" }, "There is no dataframe.")))));
};
exports.DataImport = DataImport;
//# sourceMappingURL=dataimport.js.map

/***/ })

}]);
//# sourceMappingURL=lib_index_js.0854f12a00abb03942e4.js.map