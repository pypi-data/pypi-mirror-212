(self["webpackChunkasqlcell"] = self["webpackChunkasqlcell"] || []).push([["lib_WidgetModel_js"],{

/***/ "./lib/WidgetModel.js":
/*!****************************!*\
  !*** ./lib/WidgetModel.js ***!
  \****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.SqlCellView = exports.SqlCellModel = void 0;
const widgets = __importStar(__webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base"));
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const react_dom_1 = __importDefault(__webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom"));
const WidgetView_1 = __importDefault(__webpack_require__(/*! ./WidgetView */ "./lib/WidgetView.js"));
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const defaultModelProperties = {
    data_name: "",
    dfs_button: "",
    error: ["", ""],
    exec_time: "",
    output_var: "sqlcelldf",
    row_range: [0, 10],
    column_sort: ["", 0],
    dfs_result: "",
    sql_button: "",
    mode: "",
    data_grid: "",
    data_sql: "",
    quickv_sql: "",
    quickv_data: "",
    vis_sql: ["", ""],
    vis_data: "",
    title_hist: "",
    cache: "[{}]",
};
class SqlCellModel extends widgets.DOMWidgetModel {
    constructor() {
        super(...arguments);
        this.defaults = () => {
            return Object.assign(Object.assign({}, super.defaults()), { _model_name: SqlCellModel.model_name, _model_module: SqlCellModel.model_module, _model_module_version: SqlCellModel.model_module_version, _view_name: SqlCellModel.view_name, _view_module: SqlCellModel.view_module, _view_module_version: SqlCellModel.view_module_version, output_var: "sqlcelldf", row_range: undefined, column_sort: undefined, dfs_button: undefined, dfs_result: undefined, sql_button: undefined, mode: undefined, exec_time: "", data_grid: undefined, data_name: undefined, data_sql: undefined, error: undefined, quickv_var: undefined, quickv_data: undefined, vis_sql: undefined, vis_data: undefined, title_hist: undefined, cache: undefined });
        };
    }
    initialize(attributes, options) {
        super.initialize(attributes, options);
        this.set("json_dump", new Date().toISOString());
        this.save_changes();
    }
}
exports.SqlCellModel = SqlCellModel;
SqlCellModel.serializers = Object.assign({}, widgets.DOMWidgetModel.serializers);
SqlCellModel.model_name = "SqlCellModel";
SqlCellModel.model_module = version_1.MODULE_NAME;
SqlCellModel.model_module_version = version_1.MODULE_VERSION;
SqlCellModel.view_name = "SqlCellView"; // Set to null if no view
SqlCellModel.view_module = version_1.MODULE_NAME; // Set to null if no view
SqlCellModel.view_module_version = version_1.MODULE_VERSION;
class SqlCellView extends base_1.DOMWidgetView {
    constructor() {
        super(...arguments);
        this.render = () => {
            this.el.classList.add("custom-widget");
            const component = react_1.default.createElement(WidgetView_1.default, {
                model: this.model,
            });
            react_dom_1.default.render(component, this.el);
        };
    }
}
exports.SqlCellView = SqlCellView;
//# sourceMappingURL=WidgetModel.js.map

/***/ }),

/***/ "./lib/WidgetView.js":
/*!***************************!*\
  !*** ./lib/WidgetView.js ***!
  \***************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

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
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const hooks_1 = __webpack_require__(/*! ./hooks */ "./lib/hooks.js");
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const table_1 = __webpack_require__(/*! ./table */ "./lib/table/index.js");
const visualization_1 = __webpack_require__(/*! ./visualization */ "./lib/visualization/index.js");
const icons_react_1 = __webpack_require__(/*! @tabler/icons-react */ "webpack/sharing/consume/default/@tabler/icons-react/@tabler/icons-react");
const ReactWidget = () => {
    var _a;
    const model = hooks_1.useModel();
    const [data, setData] = react_1.useState(model === null || model === void 0 ? void 0 : model.get("data_grid"));
    const [error, setError] = react_1.useState((model === null || model === void 0 ? void 0 : model.get("error")) ? model === null || model === void 0 ? void 0 : model.get("error")[0] : "");
    const [rowNumber, setRowNumber] = react_1.useState((model === null || model === void 0 ? void 0 : model.get("row_range")[1]) - (model === null || model === void 0 ? void 0 : model.get("row_range")[0]));
    const [page, setPage] = react_1.useState(Math.floor((model === null || model === void 0 ? void 0 : model.get("row_range")[0]) / rowNumber) + 1);
    const [cache, setCache] = hooks_1.useModelState("cache");
    const cacheObject = JSON.parse(cache === "" ? "{ }" : cache);
    const [tabValue, setTabValue] = react_1.useState((_a = cacheObject.tabValue) !== null && _a !== void 0 ? _a : "table");
    // Receive event from Model
    model === null || model === void 0 ? void 0 : model.on("change:error", () => {
        setError((model === null || model === void 0 ? void 0 : model.get("error")) ? model === null || model === void 0 ? void 0 : model.get("error")[0] : "");
        setData("");
    });
    model === null || model === void 0 ? void 0 : model.on("change:data_grid", () => {
        setData(model === null || model === void 0 ? void 0 : model.get("data_grid"));
        setError("");
    });
    model === null || model === void 0 ? void 0 : model.on("sort", (msg) => {
        model === null || model === void 0 ? void 0 : model.set("column_sort", msg, "");
        model === null || model === void 0 ? void 0 : model.save_changes();
    });
    model === null || model === void 0 ? void 0 : model.on("setRange", (msg) => {
        model === null || model === void 0 ? void 0 : model.set("row_range", msg, "");
        model === null || model === void 0 ? void 0 : model.save_changes();
    });
    model === null || model === void 0 ? void 0 : model.on("quick_view", (col_name) => {
        model === null || model === void 0 ? void 0 : model.set("quickv_var", [
            col_name,
            new Date().toISOString()
        ]);
        model === null || model === void 0 ? void 0 : model.save_changes();
    });
    model === null || model === void 0 ? void 0 : model.on("output_var", (outputName) => {
        model === null || model === void 0 ? void 0 : model.set("output_var", outputName);
        model === null || model === void 0 ? void 0 : model.save_changes();
    });
    model === null || model === void 0 ? void 0 : model.on("dfs_button", () => {
        model === null || model === void 0 ? void 0 : model.set("dfs_button", new Date().toISOString());
        model === null || model === void 0 ? void 0 : model.save_changes();
    });
    model === null || model === void 0 ? void 0 : model.on("data_sql", (sqlContent) => {
        model === null || model === void 0 ? void 0 : model.set("data_sql", sqlContent);
        model === null || model === void 0 ? void 0 : model.save_changes();
    });
    return (react_1.default.createElement("div", { className: "Widget" },
        react_1.default.createElement(core_1.Stack, { spacing: 0, align: "center" },
            error !== "" ?
                react_1.default.createElement(core_1.Group, { position: "left" },
                    react_1.default.createElement(core_1.Text, { color: "red" }, "Error:"),
                    react_1.default.createElement(core_1.Text, null, error))
                :
                    react_1.default.createElement(react_1.default.Fragment, null),
            data !== "" ?
                react_1.default.createElement(core_1.Group, { sx: { marginBottom: "1rem", width: "95%" }, position: "center" },
                    react_1.default.createElement(core_1.Tabs, { defaultValue: "table", value: tabValue, sx: { width: "100%" }, onTabChange: (value) => {
                            cacheObject["tabValue"] = value;
                            setCache(JSON.stringify(cacheObject));
                            setTabValue(value);
                        } },
                        react_1.default.createElement(core_1.Tabs.List, null,
                            react_1.default.createElement(core_1.Tabs.Tab, { value: "table", icon: react_1.default.createElement(icons_react_1.IconTable, { size: "0.8rem" }) }, "Table"),
                            react_1.default.createElement(core_1.Tabs.Tab, { value: "visualization", icon: react_1.default.createElement(icons_react_1.IconChartBar, { size: "0.8rem" }) }, "Visualization")),
                        react_1.default.createElement(core_1.Tabs.Panel, { value: "table" },
                            react_1.default.createElement(table_1.DataTable, { page: page, setPage: setPage, rowNumber: rowNumber, setRowNumber: setRowNumber })),
                        react_1.default.createElement(core_1.Tabs.Panel, { value: "visualization" },
                            react_1.default.createElement(visualization_1.Visualization, null))))
                :
                    react_1.default.createElement(core_1.Box, { sx: { height: "60px" } }))));
};
const withModelContext = (Component) => {
    return (props) => (react_1.default.createElement(hooks_1.WidgetModelContext.Provider, { value: props.model },
        react_1.default.createElement(Component, Object.assign({}, props))));
};
exports["default"] = withModelContext(ReactWidget);
//# sourceMappingURL=WidgetView.js.map

/***/ }),

/***/ "./lib/hooks.js":
/*!**********************!*\
  !*** ./lib/hooks.js ***!
  \**********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.useModel = exports.useModelEvent = exports.useModelState = exports.WidgetModelContext = void 0;
const react_1 = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
exports.WidgetModelContext = react_1.createContext(undefined);
// HOOKS
//============================================================================================
/**
 *
 * @param name property name in the Python model object.
 * @returns model state and set state function.
 */
function useModelState(name) {
    const model = useModel();
    const [state, setState] = react_1.useState(model === null || model === void 0 ? void 0 : model.get(name));
    useModelEvent(`change:${name}`, (model) => {
        setState(model.get(name));
    }, [name]);
    function updateModel(val, options) {
        model === null || model === void 0 ? void 0 : model.set(name, val, options);
        model === null || model === void 0 ? void 0 : model.save_changes();
    }
    return [state, updateModel];
}
exports.useModelState = useModelState;
/**
 * Subscribes a listener to the model event loop.
 * @param event String identifier of the event that will trigger the callback.
 * @param callback Action to perform when event happens.
 * @param deps Dependencies that should be kept up to date within the callback.
 */
function useModelEvent(event, callback, deps) {
    const model = useModel();
    const dependencies = deps === undefined ? [model] : [...deps, model];
    react_1.useEffect(() => {
        const callbackWrapper = (e) => model && callback(model, e);
        model === null || model === void 0 ? void 0 : model.on(event, callbackWrapper);
        return () => void (model === null || model === void 0 ? void 0 : model.unbind(event, callbackWrapper));
    }, dependencies);
}
exports.useModelEvent = useModelEvent;
/**
 * An escape hatch in case you want full access to the model.
 * @returns Python model
 */
function useModel() {
    return react_1.useContext(exports.WidgetModelContext);
}
exports.useModel = useModel;
//# sourceMappingURL=hooks.js.map

/***/ }),

/***/ "./lib/menu/index.js":
/*!***************************!*\
  !*** ./lib/menu/index.js ***!
  \***************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

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
__exportStar(__webpack_require__(/*! ./xaixs */ "./lib/menu/xaixs.js"), exports);
__exportStar(__webpack_require__(/*! ./yseries */ "./lib/menu/yseries.js"), exports);
//# sourceMappingURL=index.js.map

/***/ }),

/***/ "./lib/menu/xaixs.js":
/*!***************************!*\
  !*** ./lib/menu/xaixs.js ***!
  \***************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.XAxisSelection = void 0;
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const hooks_1 = __webpack_require__(/*! @mantine/hooks */ "webpack/sharing/consume/default/@mantine/hooks/@mantine/hooks?07de");
const icons_react_1 = __webpack_require__(/*! @tabler/icons-react */ "webpack/sharing/consume/default/@tabler/icons-react/@tabler/icons-react");
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const react_2 = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
const hooks_2 = __webpack_require__(/*! ../hooks */ "./lib/hooks.js");
const public_1 = __webpack_require__(/*! ../public */ "./lib/public/index.js");
const SamplingIndicator = () => {
    const [opened, { close, open }] = hooks_1.useDisclosure(false);
    return (react_1.default.createElement(core_1.Popover, { opened: opened },
        react_1.default.createElement(core_1.Popover.Target, null,
            react_1.default.createElement(icons_react_1.IconAlertSquareRounded, { onMouseEnter: open, onMouseLeave: close, size: 16 })),
        react_1.default.createElement(core_1.Popover.Dropdown, null,
            react_1.default.createElement(core_1.Text, { size: 8 }, "Data has been sampled."))));
};
const XAxisSelection = ({ XAxis, setXAxis, cacheObject, colName }) => {
    var _a;
    const model = hooks_2.useModel();
    const [sortAsce, setSortAsce] = react_2.useState(true);
    const [hist] = hooks_2.useModelState("title_hist");
    const headers = JSON.parse(hist !== null && hist !== void 0 ? hist : `{"columnName":"", "dtype":""}`);
    const [xAxisIcon, setXAxisIcon] = react_2.useState(react_1.default.createElement(icons_react_1.Icon123, null));
    const [cache, setCache] = hooks_2.useModelState("cache");
    const dataLength = ((_a = model === null || model === void 0 ? void 0 : model.get("data_grid")) !== null && _a !== void 0 ? _a : "{}").split("\n")[1] || 0;
    const [orient, setOrient] = react_2.useState(JSON.parse(cache.includes("chartState")
        ?
            cache
        :
            `{"chartState":{"orient": "vertical"}}`).chartState.orient);
    const headerWithType = [{ columnName: "Index(Default)", dtype: "int" }, ...headers]
        .filter(item => (item.dtype !== "int" && item.dtype !== "float") || item.columnName === "Index(Default)")
        .map((header) => {
        return ({
            value: header.columnName === "Index(Default)" ? "Index" : header.columnName, label: header.columnName, icon: public_1.IconMap[header.dtype]
        });
    });
    return (react_1.default.createElement(core_1.Grid.Col, { span: 12 },
        react_1.default.createElement(core_1.Accordion, { chevronPosition: "left", variant: "filled", sx: {
                padding: 0,
                ".mantine-Accordion-control": {
                    padding: 0,
                },
                ".mantine-Accordion-content": {
                    padding: "0.5rem 1rem 0rem 1rem",
                },
                ".mantine-Accordion-item": {
                    paddingTop: "0.5rem",
                },
            } },
            react_1.default.createElement(core_1.Accordion.Item, { value: "X-axis" },
                react_1.default.createElement(core_1.Accordion.Control, null,
                    react_1.default.createElement(core_1.Group, { noWrap: true },
                        react_1.default.createElement(core_1.Text, { size: "sm" }, "X-axis"),
                        dataLength > 500 ?
                            react_1.default.createElement(SamplingIndicator, null)
                            :
                                react_1.default.createElement(react_1.default.Fragment, null))),
                react_1.default.createElement(core_1.Accordion.Panel, null,
                    react_1.default.createElement(core_1.Grid, null,
                        react_1.default.createElement(core_1.Grid.Col, { span: 12 },
                            react_1.default.createElement(core_1.Select, { size: "xs", icon: xAxisIcon, defaultValue: "Index", value: XAxis, data: headerWithType, itemComponent: public_1.SelectItem, maxDropdownHeight: 5 * 16, onChange: (value) => {
                                    setXAxisIcon(headerWithType.filter(item => item.value === value)[0].icon);
                                    cacheObject["xAxisState"] = value;
                                    setCache(JSON.stringify(cacheObject));
                                    setXAxis(value);
                                    let array = [...colName];
                                    array = array.filter(item => item !== "");
                                    public_1.sendVisSql(model, value, array);
                                } })),
                        react_1.default.createElement(core_1.Grid.Col, { span: 8 }),
                        react_1.default.createElement(core_1.Grid.Col, { span: 2, sx: { paddingTop: 0 } },
                            react_1.default.createElement(core_1.ActionIcon, { onClick: () => {
                                    if (cache.includes("chartState")) {
                                        orient === "vertical"
                                            ?
                                                cacheObject["chartState"] = { "orient": "horizontal" }
                                            :
                                                cacheObject["chartState"] = { "orient": "vertical" };
                                    }
                                    else {
                                        cacheObject["chartState"] = JSON.parse(`{"orient":"horizontal"}`);
                                    }
                                    setCache(JSON.stringify(cacheObject));
                                    setOrient(orient === "vertical" ? "horizontal" : "vertical");
                                } }, orient === "vertical" ?
                                react_1.default.createElement(icons_react_1.IconChartArrowsVertical, { size: 16 })
                                :
                                    react_1.default.createElement(icons_react_1.IconChartArrows, { size: 16 }))),
                        react_1.default.createElement(core_1.Grid.Col, { span: 2, sx: { paddingTop: 0, display: "flex", alignItems: "center" } },
                            react_1.default.createElement(core_1.ActionIcon, { variant: "subtle", size: "xs", onClick: () => {
                                    setSortAsce(!sortAsce);
                                    model === null || model === void 0 ? void 0 : model.trigger("sort-X");
                                } }, sortAsce ?
                                react_1.default.createElement(icons_react_1.IconSortAscending, { size: 16 })
                                :
                                    react_1.default.createElement(icons_react_1.IconSortDescending, { size: 16 })))))))));
};
exports.XAxisSelection = XAxisSelection;
//# sourceMappingURL=xaixs.js.map

/***/ }),

/***/ "./lib/menu/yseries.js":
/*!*****************************!*\
  !*** ./lib/menu/yseries.js ***!
  \*****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.SelectDropDown = void 0;
const react_1 = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const icons_react_1 = __webpack_require__(/*! @tabler/icons-react */ "webpack/sharing/consume/default/@tabler/icons-react/@tabler/icons-react");
const hooks_1 = __webpack_require__(/*! ../hooks */ "./lib/hooks.js");
const public_1 = __webpack_require__(/*! ../public */ "./lib/public/index.js");
const react_2 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const SelectDropDown = ({ index, name, seriesName, setColArray, XAxis }) => {
    const [showedButton, setShowedButton] = react_1.useState(false);
    const model = hooks_1.useModel();
    const [cache, setCache] = hooks_1.useModelState("cache");
    const cacheObject = JSON.parse(cache === "" ?
        public_1.InitialSelectedCols
        :
            cache);
    if (!cacheObject["selectedCol"]) {
        cacheObject["selectedCol"] = [public_1.InitialSingleSelectedCol];
    }
    const [hist] = hooks_1.useModelState("title_hist");
    const headers = JSON.parse(hist !== null && hist !== void 0 ? hist : `{"columnName":"", "dtype":""}`);
    const headerWithType = headers
        .filter((item) => item.dtype === "int" || item.dtype === "float")
        .map((header) => {
        return ({
            value: header.columnName === "Index(Default)" ? "Index" : header.columnName, label: header.columnName, icon: public_1.IconMap[header.dtype]
        });
    });
    const [seriesIcon, setSeriesIcon] = react_1.useState(react_2.default.createElement(icons_react_1.Icon123, null));
    const target = cacheObject["selectedCol"].find((item) => item.seriesName === seriesName);
    const [chartIcon, setChartIcon] = react_1.useState(public_1.ChartIconMap[target ? target.chartType : "line"]);
    const [yAxis, setYAxis] = react_1.useState(target ? target.yAxis : "left");
    const [openRenaming, setOpenRenaming] = react_1.useState(false);
    const [seriesNameState, setSeriesNameState] = react_1.useState(seriesName);
    const seriesNames = cacheObject.selectedCol.map((item) => { return (item.seriesName); });
    react_1.useEffect(() => {
        if (target) {
            setChartIcon(public_1.ChartIconMap[target.chartType]);
        }
    }, [target]);
    return (react_2.default.createElement(core_1.Grid.Col, { span: 12, onMouseMove: () => { setShowedButton(true); }, onMouseLeave: () => setShowedButton(false) },
        react_2.default.createElement(core_1.Accordion, { chevronPosition: "left", variant: "filled", sx: {
                padding: 0,
                ".mantine-Accordion-control": {
                    width: "90%",
                    padding: 0,
                },
                ".mantine-Accordion-content": {
                    padding: "0.5rem 1rem 0rem 1rem",
                },
                ".mantine-Accordion-item": {
                    paddingTop: "0.5rem",
                },
            } },
            react_2.default.createElement(core_1.Accordion.Item, { value: `Y-series ${index}` },
                react_2.default.createElement(core_1.Group, { noWrap: true, sx: { gap: "0" } },
                    react_2.default.createElement(core_1.Accordion.Control, null,
                        react_2.default.createElement(core_1.Text, { size: "sm" }, seriesName)),
                    react_2.default.createElement(core_1.Transition, { mounted: showedButton, transition: "fade", duration: 200, timingFunction: "ease" }, (styles) => (react_2.default.createElement(core_1.ActionIcon, { style: Object.assign({}, styles), size: "xs", color: "blue", onClick: () => {
                            var array = [...cacheObject["selectedCol"]];
                            array.splice(index, 1);
                            setColArray([...array]);
                            public_1.sendVisSql(model, XAxis, array);
                            cacheObject["selectedCol"] = [...array];
                            setCache(JSON.stringify(cacheObject));
                        } },
                        react_2.default.createElement(icons_react_1.IconMinus, { size: "0.75rem" }))))),
                react_2.default.createElement(core_1.Accordion.Panel, null,
                    react_2.default.createElement(core_1.Grid, null,
                        react_2.default.createElement(core_1.Grid.Col, { span: 12 },
                            react_2.default.createElement(core_1.Select, { size: "xs", value: name, icon: seriesIcon, maxDropdownHeight: 5 * 16, itemComponent: public_1.SelectItem, data: headerWithType, sx: {
                                    ".mantine-Select-itemsWrapper": {
                                        maxWidth: "207px" // Given width of dropdown item according to fixed width of menu list
                                    }
                                }, onChange: (value) => {
                                    setSeriesIcon(headerWithType.filter(item => item.value === value)[0].icon);
                                    var names = cacheObject["selectedCol"].map((item) => item.colName);
                                    var array = [...cacheObject["selectedCol"]];
                                    array.splice(index, 1, { seriesName: seriesNameState, colName: value, chartType: target.chartType, yAxis: "left" });
                                    names.splice(index, 1, value);
                                    cacheObject["selectedCol"] = [...array];
                                    setCache(JSON.stringify(cacheObject));
                                    setColArray([...array]);
                                    public_1.sendVisSql(model, XAxis, array);
                                } })),
                        react_2.default.createElement(core_1.Grid.Col, { span: 6 }),
                        react_2.default.createElement(core_1.Grid.Col, { span: 2, sx: {
                                display: "flex",
                                justifyContent: "center"
                            } },
                            react_2.default.createElement(core_1.ActionIcon, { size: "xs", color: "darkgray" },
                                react_2.default.createElement(core_1.Popover, { opened: openRenaming },
                                    react_2.default.createElement(core_1.Popover.Target, null,
                                        react_2.default.createElement(core_1.ActionIcon, { onClick: () => setOpenRenaming(!openRenaming) },
                                            react_2.default.createElement(icons_react_1.IconEdit, { size: 16 }))),
                                    react_2.default.createElement(core_1.Popover.Dropdown, null,
                                        react_2.default.createElement(core_1.TextInput, { autoFocus: true, size: "xs", value: seriesNameState, error: target && seriesNames.includes(seriesNameState) && target.seriesName !== seriesNameState
                                                ?
                                                    react_2.default.createElement(core_1.Text, { sx: { fontSize: "x-small" } }, "No duplicated series name.")
                                                :
                                                    "", rightSection: react_2.default.createElement(core_1.Group, { noWrap: true, sx: { gap: 0 } },
                                                react_2.default.createElement(core_1.ActionIcon, { size: "xs", variant: "transparent", onClick: () => {
                                                        if (target && !seriesNames.includes(seriesNameState)) {
                                                            target.seriesName = seriesNameState;
                                                            cacheObject["selectedCol"] = [...cacheObject["selectedCol"]];
                                                            setColArray([...cacheObject["selectedCol"]]);
                                                            setCache(JSON.stringify(cacheObject));
                                                        }
                                                        setOpenRenaming(!openRenaming);
                                                    } },
                                                    react_2.default.createElement(icons_react_1.IconCheck, { size: 10 })),
                                                react_2.default.createElement(core_1.ActionIcon, { size: "xs", variant: "transparent", onClick: () => {
                                                        setOpenRenaming(!openRenaming);
                                                        setSeriesNameState(seriesName);
                                                    } },
                                                    react_2.default.createElement(icons_react_1.IconX, { size: 10 }))), onChange: (e) => setSeriesNameState(e.target.value), onKeyDown: (event) => {
                                                switch (event.key) {
                                                    case "Enter":
                                                        if (target && !seriesNames.includes(seriesNameState)) {
                                                            target.seriesName = seriesNameState;
                                                            cacheObject["selectedCol"] = [...cacheObject["selectedCol"]];
                                                            setColArray([...cacheObject["selectedCol"]]);
                                                            setCache(JSON.stringify(cacheObject));
                                                        }
                                                        setOpenRenaming(!openRenaming);
                                                        break;
                                                    case "Escape":
                                                        setOpenRenaming(!openRenaming);
                                                        setSeriesNameState(seriesName);
                                                        break;
                                                }
                                            } }))))),
                        react_2.default.createElement(core_1.Grid.Col, { span: 2, sx: {
                                display: "flex",
                                justifyContent: "center"
                            } },
                            react_2.default.createElement(core_1.Select, { size: "xs", rightSectionProps: { display: "none" }, itemComponent: public_1.SelectItem, data: [
                                    { value: "line", label: "Line", icon: public_1.ChartIconMap["line"] },
                                    { value: "bar", label: "Bar", icon: public_1.ChartIconMap["bar"] },
                                    { value: "point", label: "Point", icon: public_1.ChartIconMap["point"] },
                                    { value: "arc", label: "Pie", icon: public_1.ChartIconMap["arc"] },
                                ], icon: chartIcon, sx: {
                                    ".mantine-Select-icon": {
                                        alignItems: "flex-start",
                                    },
                                    ".mantine-Select-rightSection": {
                                        display: "none",
                                    },
                                    ".mantine-Select-input": {
                                        backgroundColor: "transparent",
                                        border: "none",
                                        paddingLeft: 0,
                                        color: "transparent"
                                    },
                                    ".mantine-Select-dropdown": {
                                        width: "6rem !important"
                                    }
                                }, onChange: (value) => {
                                    setChartIcon(public_1.ChartIconMap[value]);
                                    if (!target) {
                                        return;
                                    }
                                    target.chartType = value;
                                    cacheObject["selectedCol"] = [...cacheObject["selectedCol"]];
                                    setColArray([...cacheObject["selectedCol"]]);
                                    setCache(JSON.stringify(cacheObject));
                                } })),
                        react_2.default.createElement(core_1.Grid.Col, { span: 2, sx: {
                                display: "flex",
                                justifyContent: "center"
                            } },
                            react_2.default.createElement(core_1.ActionIcon, { size: "xs", onClick: () => {
                                    const value = yAxis === "left" ? "right" : "left";
                                    setYAxis(value);
                                    if (!target) {
                                        return;
                                    }
                                    target.yAxis = value;
                                    cacheObject["selectedCol"] = [...cacheObject["selectedCol"]];
                                    setCache(JSON.stringify(cacheObject));
                                } }, yAxis === "left" ?
                                react_2.default.createElement(icons_react_1.IconBorderLeft, { size: 16 })
                                :
                                    react_2.default.createElement(icons_react_1.IconBorderRight, { size: 16 })))))))));
};
exports.SelectDropDown = SelectDropDown;
//# sourceMappingURL=yseries.js.map

/***/ }),

/***/ "./lib/public/function.js":
/*!********************************!*\
  !*** ./lib/public/function.js ***!
  \********************************/
/***/ ((__unused_webpack_module, exports) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.sendVisSql = void 0;
// The reason why we pass model as a parameter into this function is 
// it would cause an error if we get model by useModel here. 
const sendVisSql = (model, ColName, array) => {
    const isIndex = ColName === "Index";
    const group = array
        .filter((item) => (item.colName !== ""))
        .map((item) => (`"${item.colName}"`));
    model === null || model === void 0 ? void 0 : model.set("vis_sql", [
        // NOTE: THE CONDITION WOULD ALWAYS BE TRUE
        `select * EXCLUDE (index_rn1qaz2wsx)\nfrom \n(\nSELECT ${group.join(",")}${!isIndex ? "," + `"${ColName}"` : ""}, ROW_NUMBER() OVER () AS index_rn1qaz2wsx\n FROM $$__NAME__$$ ${ true ? "" : 0}\n)\nusing SAMPLE reservoir (500 rows) REPEATABLE(42)\norder by index_rn1qaz2wsx`,
        isIndex ? "index_rn1qaz2wsx" : ColName,
        new Date().toISOString()
    ]);
    model === null || model === void 0 ? void 0 : model.save_changes();
};
exports.sendVisSql = sendVisSql;
//# sourceMappingURL=function.js.map

/***/ }),

/***/ "./lib/public/index.js":
/*!*****************************!*\
  !*** ./lib/public/index.js ***!
  \*****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

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
__exportStar(__webpack_require__(/*! ./variable */ "./lib/public/variable.js"), exports);
__exportStar(__webpack_require__(/*! ./function */ "./lib/public/function.js"), exports);
//# sourceMappingURL=index.js.map

/***/ }),

/***/ "./lib/public/variable.js":
/*!********************************!*\
  !*** ./lib/public/variable.js ***!
  \********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

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
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.SelectItem = exports.ChartType = exports.IconMap = exports.ChartIconMap = exports.InitialSelectedCols = exports.InitialSingleSelectedCol = void 0;
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const icons_react_1 = __webpack_require__(/*! @tabler/icons-react */ "webpack/sharing/consume/default/@tabler/icons-react/@tabler/icons-react");
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
exports.InitialSingleSelectedCol = { "seriesName": "Y-series-0", "colName": "", "chartType": "line", "yAxis": "left" };
exports.InitialSelectedCols = `{"selectedCol":[{"seriesName":"Y-series-0", "colName":"","chartType":"line", "yAxis":"left"}]}`;
exports.ChartIconMap = {
    "line": react_1.default.createElement(icons_react_1.IconChartLine, { size: 16 }),
    "bar": react_1.default.createElement(icons_react_1.IconChartBar, { size: 16 }),
    "point": react_1.default.createElement(icons_react_1.IconChartDots, { size: 16 }),
    "arc": react_1.default.createElement(icons_react_1.IconChartPie, { size: 16 })
};
exports.IconMap = {
    "int": react_1.default.createElement(icons_react_1.Icon123, { size: 16 }),
    "float": react_1.default.createElement(icons_react_1.Icon123, { size: 16 }),
    "string": react_1.default.createElement(icons_react_1.IconAbc, { size: 16 }),
    "bool": react_1.default.createElement(icons_react_1.IconAbc, { size: 16 }),
    "datetime": react_1.default.createElement(icons_react_1.IconCalendar, { size: 16 }),
};
exports.ChartType = {
    Line: "line",
    Bar: "bar",
    Scatter: "point",
    Pie: "arc"
};
exports.SelectItem = react_1.forwardRef((_a, ref) => {
    var { label, icon } = _a, others = __rest(_a, ["label", "icon"]);
    return (react_1.default.createElement("div", Object.assign({ ref: ref }, others),
        react_1.default.createElement(core_1.Group, { noWrap: true, position: "apart", w: "100%" },
            react_1.default.createElement(core_1.Group, { sx: { width: "60%" } },
                react_1.default.createElement(core_1.Text, { truncate: true, size: "xs" }, label)),
            icon)));
});
//# sourceMappingURL=variable.js.map

/***/ }),

/***/ "./lib/table/element.js":
/*!******************************!*\
  !*** ./lib/table/element.js ***!
  \******************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.TableElement = void 0;
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const vsc_1 = __webpack_require__(/*! react-icons/vsc */ "./node_modules/react-icons/vsc/index.esm.js");
const hooks_1 = __webpack_require__(/*! @mantine/hooks */ "webpack/sharing/consume/default/@mantine/hooks/@mantine/hooks?07de");
const TableElement = ({ item }) => {
    const { ref, width } = hooks_1.useElementSize();
    return (react_1.default.createElement(core_1.Popover, { position: "top", withArrow: true, shadow: "md" },
        react_1.default.createElement(core_1.Group, { ref: ref, noWrap: true, sx: { gap: 0 } },
            react_1.default.createElement(core_1.Text, { sx: { overflow: "hidden" }, fz: "8px" }, item.substring(0, width / 8)),
            react_1.default.createElement(core_1.Popover.Target, null, width < (8 * item.length - 40) ?
                react_1.default.createElement(core_1.ActionIcon, { variant: "light", color: "blue", sx: { height: "10px", minHeight: "10px", width: "10px", minWidth: "10px" } },
                    react_1.default.createElement(vsc_1.VscEllipsis, { size: 8 }))
                :
                    react_1.default.createElement("div", null))),
        react_1.default.createElement(core_1.Popover.Dropdown, { sx: { padding: 0 } },
            react_1.default.createElement(core_1.Textarea, { readOnly: true, variant: "unstyled", withAsterisk: true, defaultValue: item, autosize: true, minRows: 1, maxRows: 2, sx: {
                    fontSize: "12px",
                    "& .mantine-Textarea-input": {
                        cursor: "default",
                        paddingTop: 0,
                        paddingBottom: 0,
                    }
                } }))));
};
exports.TableElement = TableElement;
//# sourceMappingURL=element.js.map

/***/ }),

/***/ "./lib/table/header.js":
/*!*****************************!*\
  !*** ./lib/table/header.js ***!
  \*****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

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
exports.DataframeHeader = void 0;
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const icons_react_1 = __webpack_require__(/*! @tabler/icons-react */ "webpack/sharing/consume/default/@tabler/icons-react/@tabler/icons-react");
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const fa_1 = __webpack_require__(/*! react-icons/fa */ "./node_modules/react-icons/fa/index.esm.js");
const hooks_1 = __webpack_require__(/*! ../hooks */ "./lib/hooks.js");
const visualization_1 = __webpack_require__(/*! ../visualization */ "./lib/visualization/index.js");
const HeaderInfo = ({ headerContent, item, dataLength }) => {
    const model = hooks_1.useModel();
    const [open, setOpen] = react_1.useState(undefined);
    return (react_1.default.createElement(react_1.default.Fragment, null, headerContent.filter(header => header.columnName === item && (header.dtype.includes("int") || header.dtype.includes("float"))).length !== 0 ?
        react_1.default.createElement(core_1.Group, { noWrap: true, position: "center", sx: { gap: 0, alignItems: "flex-start" } },
            react_1.default.createElement(visualization_1.HistChart, { item: item, headerContent: headerContent }),
            react_1.default.createElement(core_1.Popover, { onOpen: () => {
                    model === null || model === void 0 ? void 0 : model.trigger("quick_view", item);
                } },
                react_1.default.createElement(core_1.Popover.Target, null,
                    react_1.default.createElement(core_1.ActionIcon, { variant: "transparent", sx: { alignItems: "flex-end" } },
                        react_1.default.createElement(icons_react_1.IconChartLine, { size: 12 }))),
                react_1.default.createElement(core_1.Popover.Dropdown, { sx: {
                        position: "fixed",
                        top: "calc(50vh - 75px) !important",
                        left: "calc(50vw - 240px) !important",
                    } },
                    react_1.default.createElement(visualization_1.QuickViewChart, null))))
        :
            react_1.default.createElement(core_1.Stack, { align: "left", sx: { gap: 0 } }, headerContent.filter(header => header.columnName === item).length > 0 ?
                headerContent.filter(header => header.columnName === item)[0].bins.map((bin, index) => {
                    return (react_1.default.createElement(core_1.Group, { key: index, noWrap: true, position: "apart", onMouseEnter: () => { setOpen(item); }, onMouseLeave: () => setOpen(undefined), sx: { gap: 0, width: "10rem", marginBottom: "-2px" } }, bin.count !== 0 ?
                        react_1.default.createElement(react_1.default.Fragment, null,
                            react_1.default.createElement(core_1.Box, { sx: { maxWidth: "6rem" } },
                                react_1.default.createElement(core_1.Text, { weight: 600, fs: "italic", c: "#696969", truncate: true, fz: "xs" }, bin.bin)),
                            open ?
                                react_1.default.createElement(core_1.Text, { c: "blue", fz: "xs" }, bin.count)
                                :
                                    react_1.default.createElement(core_1.Text, { c: "blue", fz: "xs" },
                                        (bin.count / dataLength * 100).toFixed(2),
                                        "%"))
                        :
                            react_1.default.createElement(react_1.default.Fragment, null)));
                })
                :
                    react_1.default.createElement(react_1.default.Fragment, null))));
};
const HeaderTitle = ({ headerContent, item }) => {
    const model = hooks_1.useModel();
    const Order = {
        Increasing: 1,
        Descending: -1,
        None: 0,
    };
    const [colSort, setColSort] = hooks_1.useModelState("column_sort");
    let currentOrder = Order.None;
    return (react_1.default.createElement(core_1.Group, { position: "center" },
        react_1.default.createElement(core_1.Button, { color: "dark", sx: {
                maxWidth: "10rem",
                height: "27px",
                "&.mantine-UnstyledButton-root": {
                    ":hover": {
                        backgroundColor: "#ebebeb",
                    }
                }
            }, rightIcon: react_1.default.createElement(react_1.default.Fragment, null,
                headerContent ?
                    headerContent.filter(header => header.columnName === item).length !== 0 ?
                        react_1.default.createElement(core_1.Text, { size: "xs", fs: "italic", color: "gray" }, headerContent.filter(header => header.columnName === item)[0].dtype.includes("datetime") ?
                            "datetime"
                            :
                                headerContent.filter(header => header.columnName === item)[0].dtype)
                        :
                            react_1.default.createElement(react_1.default.Fragment, null)
                    :
                        react_1.default.createElement(react_1.default.Fragment, null),
                colSort[0] === item ?
                    colSort[1] === Order.Increasing ?
                        react_1.default.createElement(fa_1.FaSortUp, { color: "gray", size: 10 })
                        :
                            colSort[1] === Order.Descending ?
                                react_1.default.createElement(fa_1.FaSortDown, { color: "gray", size: 10 })
                                :
                                    react_1.default.createElement(fa_1.FaSort, { color: "lightgray", size: 10 })
                    :
                        react_1.default.createElement(fa_1.FaSort, { color: "lightgray", size: 10 })), variant: "subtle", onClick: () => {
                if (colSort[0] === item) {
                    if (colSort[1] === Order.Increasing) {
                        currentOrder = Order.Descending;
                        setColSort([colSort[0], Order.Descending]);
                    }
                    else if (colSort[1] === Order.Descending) {
                        currentOrder = Order.None;
                        setColSort([colSort[0], Order.None]);
                    }
                    else {
                        currentOrder = Order.Increasing;
                        setColSort([colSort[0], Order.Increasing]);
                    }
                }
                else {
                    currentOrder = Order.Increasing;
                    setColSort([colSort[0], Order.Increasing]);
                }
                model === null || model === void 0 ? void 0 : model.trigger("sort", [item, currentOrder]);
            } },
            react_1.default.createElement(core_1.Text, { truncate: true, fw: 700 }, item))));
};
const DataframeHeader = ({ headerContent, header, dataLength }) => {
    return (react_1.default.createElement("thead", null,
        react_1.default.createElement("tr", null,
            react_1.default.createElement("th", null),
            header.map((item, index) => react_1.default.createElement("th", { key: index, style: {
                    padding: 0,
                    verticalAlign: "baseline",
                } },
                react_1.default.createElement(core_1.Box, { sx: {
                        display: "flex",
                        justifyContent: "center",
                    } },
                    react_1.default.createElement(core_1.Stack, { align: "center", sx: { gap: 0, maxWidth: "10rem" } },
                        react_1.default.createElement(HeaderTitle, { headerContent: headerContent, item: item }),
                        headerContent ?
                            react_1.default.createElement(HeaderInfo, { headerContent: headerContent, item: item, dataLength: dataLength })
                            :
                                react_1.default.createElement(react_1.default.Fragment, null))))))));
};
exports.DataframeHeader = DataframeHeader;
//# sourceMappingURL=header.js.map

/***/ }),

/***/ "./lib/table/index.js":
/*!****************************!*\
  !*** ./lib/table/index.js ***!
  \****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

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
__exportStar(__webpack_require__(/*! ./header */ "./lib/table/header.js"), exports);
__exportStar(__webpack_require__(/*! ./table */ "./lib/table/table.js"), exports);
//# sourceMappingURL=index.js.map

/***/ }),

/***/ "./lib/table/table.js":
/*!****************************!*\
  !*** ./lib/table/table.js ***!
  \****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.DataTable = void 0;
const react_1 = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const react_2 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const header_1 = __webpack_require__(/*! ./header */ "./lib/table/header.js");
const element_1 = __webpack_require__(/*! ./element */ "./lib/table/element.js");
const hooks_1 = __webpack_require__(/*! ../hooks */ "./lib/hooks.js");
const icons_react_1 = __webpack_require__(/*! @tabler/icons-react */ "webpack/sharing/consume/default/@tabler/icons-react/@tabler/icons-react");
const NumericElement = ({ item, maxItem, minItem, actived }) => {
    const percentage = maxItem !== minItem ? 1 - ((item - minItem) / (maxItem - minItem)) : 0;
    const color = 150 * percentage + 105;
    const textColor = color > 125 ? 0 : 255;
    return (react_2.default.createElement(core_1.Box, { bg: actived ? `rgb(${color}, ${color}, ${color})` : "transparent", c: actived ? `rgb(${textColor}, ${textColor}, ${textColor})` : "black" },
        react_2.default.createElement(core_1.Text, { sx: { overflow: "hidden" }, fz: "8px" }, item)));
};
const DataTable = ({ page, setPage, rowNumber, setRowNumber }) => {
    var _a, _b;
    const model = hooks_1.useModel();
    const [data, setData] = react_1.useState((_a = model === null || model === void 0 ? void 0 : model.get("data_grid")) !== null && _a !== void 0 ? _a : "{}");
    model === null || model === void 0 ? void 0 : model.on("change:data_grid", () => { setData(model.get("data_grid")); });
    const [hist] = hooks_1.useModelState("title_hist");
    const [execTime, setExecTime] = react_1.useState((_b = model === null || model === void 0 ? void 0 : model.get("exec_time")) !== null && _b !== void 0 ? _b : "");
    model === null || model === void 0 ? void 0 : model.on("execTime", (msg) => setExecTime(msg.slice(9, msg.length)));
    const [tempoIndex, setTempoIndex] = react_1.useState(1);
    const [outOfRange, setOutOfRange] = react_1.useState(false);
    const [activedFormatting, setActiedFormatting] = react_1.useState(false);
    const info = JSON.parse(data.split("\n")[0]);
    const cols = info.columns;
    const infoByCol = cols.map((item, index) => {
        return (info.data.map((item) => { return (item[index]); }));
    });
    const maxArray = infoByCol.map((item) => {
        if (typeof (item[0]) === "number") {
            return (Math.max(...item));
        }
        else {
            return (undefined);
        }
    });
    const minArray = infoByCol.map((item) => {
        if (typeof (item[0]) === "number") {
            return (Math.min(...item));
        }
        else {
            return (undefined);
        }
    });
    const dataLength = data.split("\n")[1] || 0;
    const header = info.columns;
    let timeDiff = 0;
    if (execTime.length !== 0) {
        timeDiff = (new Date(execTime.split(",")[1]).getTime() - new Date(execTime.split(",")[0]).getTime()) / 1000;
    }
    const headerContent = hist ?
        JSON.parse(hist)
        :
            [{ columnName: "", dtype: "", bins: [{ bin_start: 0, bin_end: 0, count: 0 }] }];
    const rows = [...Array(info.index.length).keys()].map((index) => (react_2.default.createElement("tr", { key: base_1.uuid() },
        react_2.default.createElement("td", { key: index }, info.index[index]),
        info.data[index].map((item, tdIndex) => (react_2.default.createElement("td", { key: tdIndex, style: { fontSize: "8px" } }, typeof (item) === "boolean" ?
            item ?
                "True"
                :
                    "False"
            :
                typeof (item) === "string" ?
                    react_2.default.createElement(element_1.TableElement, { item: item })
                    :
                        react_2.default.createElement(NumericElement, { item: item, minItem: minArray[tdIndex], maxItem: maxArray[tdIndex], actived: activedFormatting })))))));
    return (react_2.default.createElement(core_1.Stack, { align: "center", spacing: 10, sx: {
            width: "100%",
            marginBottom: "16px",
        } },
        react_2.default.createElement(core_1.ScrollArea, { scrollbarSize: 8, style: { width: "100%" } },
            react_2.default.createElement(core_1.Table, { withBorder: true, withColumnBorders: true, striped: true, sx: {
                    width: "100%",
                    "& thead": {
                        height: "57px",
                    },
                    "& td": {
                        maxWidth: "200px"
                    },
                    "& tbody tr td": {
                        padding: "0px 3px",
                    },
                    "&  td:first-of-type": {
                        backgroundColor: "#ebebeb",
                        width: "7%"
                    },
                    "&  tr:first-of-type": {
                        backgroundColor: "#ebebeb",
                    },
                    "&  tr:nth-of-type(even)": {
                        backgroundColor: "#f2f2f2",
                    },
                } },
                react_2.default.createElement(header_1.DataframeHeader, { headerContent: headerContent, header: header, dataLength: dataLength }),
                react_2.default.createElement("tbody", null, rows))),
        react_2.default.createElement(core_1.Group, { position: "apart", sx: { width: "100%" } },
            react_2.default.createElement(core_1.Group, null,
                react_2.default.createElement(core_1.Text, { color: "#8d8d8d" },
                    dataLength,
                    " rows"),
                timeDiff !== 0 ?
                    react_2.default.createElement(core_1.Text, { color: "#8d8d8d" },
                        timeDiff,
                        " s")
                    :
                        react_2.default.createElement(react_2.default.Fragment, null)),
            react_2.default.createElement(core_1.Group, { align: "center" },
                react_2.default.createElement(core_1.Tooltip, { label: "Conditional Formatting", withArrow: true },
                    react_2.default.createElement(core_1.ActionIcon, { variant: "transparent", onClick: () => { setActiedFormatting(!activedFormatting); } },
                        react_2.default.createElement(icons_react_1.IconFilters, { size: 16 }))),
                react_2.default.createElement(core_1.Group, { sx: { gap: 0 } },
                    react_2.default.createElement(core_1.Select, { sx: {
                            width: "40px",
                            height: "22px",
                            ".mantine-Select-item": { padding: "0px" },
                            ".mantine-Select-rightSection": { width: "20px" },
                            ".mantine-Select-input": {
                                paddingLeft: "1px",
                                paddingRight: "0px",
                                height: "22px",
                                minHeight: "22px",
                                color: "#8d8d8d",
                            },
                        }, placeholder: rowNumber, data: ["10", "30", "50", "100"], onChange: (number) => {
                            const num = number;
                            setPage(1);
                            setRowNumber(num);
                            model === null || model === void 0 ? void 0 : model.trigger("setRange", [(0 * num), 1 * num]);
                        } }),
                    react_2.default.createElement(core_1.Text, { color: "#8d8d8d" }, "/page")),
                data ?
                    react_2.default.createElement(core_1.Pagination, { size: "xs", page: page, total: Math.ceil(dataLength / rowNumber), onChange: (index) => {
                            setPage(index);
                            model === null || model === void 0 ? void 0 : model.trigger("setRange", [((index - 1) * rowNumber), index * rowNumber]);
                        }, styles: (theme) => ({
                            item: {
                                color: theme.colors.gray[4],
                                backgroundColor: theme.colors.gray[0],
                                "&[data-active]": {
                                    color: theme.colors.dark[2],
                                    backgroundColor: theme.colors.gray[4],
                                },
                            },
                        }) })
                    :
                        react_2.default.createElement(react_2.default.Fragment, null),
                react_2.default.createElement(core_1.Group, { sx: { gap: 0 } },
                    react_2.default.createElement(core_1.Text, { color: "#8d8d8d" }, "goto"),
                    react_2.default.createElement(core_1.NumberInput, { defaultValue: 18, size: "xs", hideControls: true, error: outOfRange, value: page, onBlur: () => {
                            if (tempoIndex > 0 && tempoIndex <= Math.ceil(dataLength / rowNumber)) {
                                setPage(tempoIndex);
                                setOutOfRange(false);
                                model === null || model === void 0 ? void 0 : model.trigger("setRange", [((tempoIndex - 1) * rowNumber), tempoIndex * rowNumber]);
                            }
                            else {
                                setOutOfRange(true);
                            }
                        }, onKeyDown: (e) => {
                            if (["Escape", "Enter"].indexOf(e.key) > -1) {
                                (document.activeElement instanceof HTMLElement) && document.activeElement.blur();
                                if (tempoIndex > 0 && tempoIndex <= Math.ceil(dataLength / rowNumber)) {
                                    setPage(tempoIndex);
                                    setOutOfRange(false);
                                    model === null || model === void 0 ? void 0 : model.trigger("setRange", [((tempoIndex - 1) * rowNumber), tempoIndex * rowNumber]);
                                }
                                else {
                                    setOutOfRange(true);
                                }
                            }
                        }, onChange: (page) => {
                            setTempoIndex(page);
                            (page > 0 && page <= Math.ceil(dataLength / rowNumber)) ?
                                setOutOfRange(false)
                                :
                                    setOutOfRange(true);
                        }, sx: {
                            width: "40px",
                            ".mantine-NumberInput-input": {
                                paddingLeft: "5px",
                                paddingRight: "0px",
                                height: "22px",
                                minHeight: "22px",
                            }
                        } }))))));
};
exports.DataTable = DataTable;
//# sourceMappingURL=table.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/visualization/const.js":
/*!************************************!*\
  !*** ./lib/visualization/const.js ***!
  \************************************/
/***/ ((__unused_webpack_module, exports) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.LabelWidth = exports.MenuWidth = exports.MenuHeight = exports.ViewHeight = void 0;
exports.ViewHeight = 264;
exports.MenuHeight = 311;
exports.MenuWidth = 285;
exports.LabelWidth = 128;
//# sourceMappingURL=const.js.map

/***/ }),

/***/ "./lib/visualization/hist.js":
/*!***********************************!*\
  !*** ./lib/visualization/hist.js ***!
  \***********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.HistChart = void 0;
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const react_vega_1 = __webpack_require__(/*! react-vega */ "webpack/sharing/consume/default/react-vega/react-vega");
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const HistChart = ({ item, headerContent }) => {
    const expo = (input) => { return input.toExponential(2); };
    const isScientific = (input) => { return (!(0.1 <= Math.abs(input) && Math.abs(input) <= 10000)); };
    const getIntervalSide = (input) => {
        let res = "";
        if (input === 0) {
            res = "0";
        }
        else if (isScientific(input)) {
            res = expo(input);
        }
        else {
            res = input.toFixed(2);
        }
        return res;
    };
    const globalInterval = (item) => {
        const left = headerContent.filter(header => header.columnName === item)[0].bins[0].bin_start;
        const right = headerContent.filter(header => header.columnName === item)[0].bins[9].bin_end;
        return (`[${getIntervalSide(left)}, ${getIntervalSide(right)}]`);
    };
    const data = headerContent.filter(header => header.columnName === item)[0].bins;
    const barData = {
        table: data.map((item, index) => {
            const leftInterval = getIntervalSide(item.bin_start);
            const rightInterval = getIntervalSide(item.bin_end);
            const interval = `[${leftInterval}, ${rightInterval}]`;
            return ({ a: interval, b: item.count, index: index });
        }),
    };
    return (react_1.default.createElement(core_1.Stack, null,
        react_1.default.createElement(react_vega_1.VegaLite, { data: barData, actions: false, renderer: 'svg', spec: {
                "background": "transparent",
                "data": { "name": "table" },
                "width": 60,
                "height": 40,
                "config": { "view": { "stroke": null } },
                "layer": [
                    {
                        "params": [
                            {
                                "name": "hover",
                                "select": { "type": "point", "on": "mouseover", "clear": "mouseout" }
                            }
                        ],
                        "mark": { "type": "bar", "color": "#eee", "tooltip": true },
                        "transform": [
                            {
                                "calculate": "datum.a + ': ' +datum.b", "as": "tooltip",
                            }
                        ],
                        "encoding": {
                            "x": {
                                "field": "index",
                                "type": "nominal",
                                "axis": { "labels": false, "title": null },
                            },
                            "tooltip": { "field": "tooltip", "type": "nominal" },
                            "opacity": {
                                "condition": { "test": { "param": "hover", "empty": false }, "value": 0.5 },
                                "value": 0
                            },
                            "detail": [{ "field": "count" }]
                        }
                    },
                    {
                        "mark": "bar",
                        "transform": [{
                                "calculate": "datum.b===0 ? 0 : datum.b === 1? 0.5: log(datum.b)/log(2)", "as": "log_x"
                            }],
                        "encoding": {
                            "x": {
                                "field": "index",
                                "type": "nominal",
                                "axis": { "labels": false, "title": null, "ticks": false },
                            },
                            "y": {
                                "field": "log_x",
                                "type": "quantitative",
                                "axis": { "labels": false, "domain": false, "grid": false, "ticks": false, "title": null },
                            },
                        }
                    },
                ]
            } }),
        react_1.default.createElement(core_1.Group, { sx: { width: "max-content" } },
            react_1.default.createElement(core_1.Text, { size: "xs", c: "#696969", sx: { marginTop: "-20px" } }, globalInterval(item)))));
};
exports.HistChart = HistChart;
//# sourceMappingURL=hist.js.map

/***/ }),

/***/ "./lib/visualization/index.js":
/*!************************************!*\
  !*** ./lib/visualization/index.js ***!
  \************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

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
__exportStar(__webpack_require__(/*! ./hist */ "./lib/visualization/hist.js"), exports);
__exportStar(__webpack_require__(/*! ./quickview */ "./lib/visualization/quickview.js"), exports);
__exportStar(__webpack_require__(/*! ./menu */ "./lib/visualization/menu.js"), exports);
__exportStar(__webpack_require__(/*! ./visualization */ "./lib/visualization/visualization.js"), exports);
__exportStar(__webpack_require__(/*! ./const */ "./lib/visualization/const.js"), exports);
//# sourceMappingURL=index.js.map

/***/ }),

/***/ "./lib/visualization/menu.js":
/*!***********************************!*\
  !*** ./lib/visualization/menu.js ***!
  \***********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

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
exports.VisualMenu = void 0;
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const icons_react_1 = __webpack_require__(/*! @tabler/icons-react */ "webpack/sharing/consume/default/@tabler/icons-react/@tabler/icons-react");
const hooks_1 = __webpack_require__(/*! ../hooks */ "./lib/hooks.js");
const menu_1 = __webpack_require__(/*! ../menu */ "./lib/menu/index.js");
const menu_2 = __webpack_require__(/*! ../menu */ "./lib/menu/index.js");
const public_1 = __webpack_require__(/*! ../public */ "./lib/public/index.js");
const const_1 = __webpack_require__(/*! ./const */ "./lib/visualization/const.js");
const VisualMenu = ({ XAxis, setXAxis }) => {
    const [cache, setCache] = hooks_1.useModelState("cache");
    const [colArray, setColArray] = react_1.useState(JSON.parse(cache.includes("selectedCol")
        ?
            cache
        :
            public_1.InitialSelectedCols).selectedCol);
    const cacheObject = JSON.parse(cache === "" ? "{ }" : cache);
    return (react_1.default.createElement(core_1.Stack, { h: "100%", sx: { minWidth: "15rem" } },
        react_1.default.createElement(core_1.Tabs, { variant: "pills", defaultValue: "data", sx: {
                ".mantine-Tabs-tabsList": {
                    height: 0
                }
            } },
            react_1.default.createElement(core_1.Tabs.List, { grow: true },
                react_1.default.createElement(core_1.Group, { noWrap: true, sx: { marginBottom: "1rem" } })),
            react_1.default.createElement(core_1.Tabs.Panel, { value: "data" },
                react_1.default.createElement(core_1.ScrollArea, { offsetScrollbars: true, dir: "rtl", h: const_1.MenuHeight, w: "100%", sx: {
                        paddingLeft: "1rem",
                    } },
                    react_1.default.createElement(core_1.Grid, { sx: {
                            direction: "ltr",
                            gap: "0",
                            marginBottom: "1.5rem",
                            maxWidth: "100%",
                            overflowX: "hidden",
                        } },
                        react_1.default.createElement(menu_1.XAxisSelection, { XAxis: XAxis, setXAxis: setXAxis, cacheObject: cacheObject, colName: colArray }),
                        colArray.map((item, index) => {
                            return (react_1.default.createElement(menu_2.SelectDropDown, { index: index, name: item.colName, seriesName: item.seriesName, colArray: colArray, setColArray: setColArray, XAxis: XAxis }));
                        }),
                        react_1.default.createElement(core_1.Grid.Col, { span: 7 }),
                        react_1.default.createElement(core_1.Grid.Col, { span: 5, sx: {
                                display: "flex",
                                justifyContent: "flex-end"
                            } },
                            react_1.default.createElement(core_1.Button, { compact: true, variant: "subtle", leftIcon: react_1.default.createElement(icons_react_1.IconPlus, { size: "0.75rem" }), size: "xs", sx: {
                                    ":hover": {
                                        color: "blue",
                                        backgroundColor: "transparent"
                                    }
                                }, onClick: () => {
                                    var names = colArray.map(item => { return (item.seriesName); });
                                    var givenName = "";
                                    colArray.forEach((col, index) => {
                                        var tempoName = `Y-series-${index}`;
                                        if (!names.includes(tempoName)) {
                                            givenName = tempoName;
                                        }
                                    });
                                    if (givenName === "") {
                                        givenName = `Y-series-${names.length}`;
                                    }
                                    colArray.splice(colArray.length, 0, { seriesName: givenName, colName: "", chartType: "line", yAxis: "left" });
                                    setColArray([...colArray]);
                                    cacheObject["selectedCol"] = [...colArray];
                                    setCache(JSON.stringify(cacheObject));
                                } }, "Add series"))))))));
};
exports.VisualMenu = VisualMenu;
//# sourceMappingURL=menu.js.map

/***/ }),

/***/ "./lib/visualization/quickview.js":
/*!****************************************!*\
  !*** ./lib/visualization/quickview.js ***!
  \****************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.QuickViewChart = void 0;
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const react_vega_1 = __webpack_require__(/*! react-vega */ "webpack/sharing/consume/default/react-vega/react-vega");
const hooks_1 = __webpack_require__(/*! ../hooks */ "./lib/hooks.js");
const QuickViewChart = () => {
    const [data] = hooks_1.useModelState("quickv_data");
    const lineData = { values: JSON.parse(data === "" ? `{"columns":[],"index":[],"data":[]}` : data) };
    const dataLength = lineData.values.length;
    return react_1.default.createElement(react_vega_1.VegaLite, { data: lineData, actions: false, renderer: 'svg', spec: {
            width: 400,
            height: 150,
            params: [{
                    name: "industry",
                    select: { type: "point", fields: ["series"] },
                    bind: "legend"
                }],
            layer: [
                {
                    mark: "line",
                    transform: [
                        { calculate: "toNumber(datum.x)", as: "index" },
                        { calculate: "datum.y", as: "y" }
                    ],
                    encoding: {
                        x: { field: "index", type: dataLength >= 10 ? "quantitative" : "ordinal", axis: { title: null } },
                        y: { field: "y", type: "quantitative" },
                        opacity: {
                            condition: { param: "industry", value: 1 },
                            value: 10
                        }
                    },
                    data: { name: "values" }
                }
            ]
        } });
};
exports.QuickViewChart = QuickViewChart;
//# sourceMappingURL=quickview.js.map

/***/ }),

/***/ "./lib/visualization/visualization.js":
/*!********************************************!*\
  !*** ./lib/visualization/visualization.js ***!
  \********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

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
exports.Visualization = void 0;
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const hooks_1 = __webpack_require__(/*! @mantine/hooks */ "webpack/sharing/consume/default/@mantine/hooks/@mantine/hooks?07de");
const icons_react_1 = __webpack_require__(/*! @tabler/icons-react */ "webpack/sharing/consume/default/@tabler/icons-react/@tabler/icons-react");
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const react_vega_1 = __webpack_require__(/*! react-vega */ "webpack/sharing/consume/default/react-vega/react-vega");
const hooks_2 = __webpack_require__(/*! ../hooks */ "./lib/hooks.js");
const const_1 = __webpack_require__(/*! ./const */ "./lib/visualization/const.js");
const menu_1 = __webpack_require__(/*! ./menu */ "./lib/visualization/menu.js");
const vega_embed_1 = __webpack_require__(/*! vega-embed */ "webpack/sharing/consume/default/vega-embed/vega-embed?f638");
const VisualPreviewChart = ({ rect, XAxis, open }) => {
    const model = hooks_2.useModel();
    const [hist] = hooks_2.useModelState("title_hist");
    const headers = JSON.parse(hist !== null && hist !== void 0 ? hist : `{"dtype":""}`);
    const dateCols = headers.filter((header) => header.dtype.includes("datetime"));
    const dateColName = dateCols.length >= 1 ? dateCols.map((item) => item.columnName) : [""];
    const [visData] = hooks_2.useModelState("vis_data");
    const lineData = { values: JSON.parse(visData === "" ? `[{ "x": 0, "y": 0, "type": 0 }]` : visData) };
    const [sortAsce, setSortAsce] = react_1.useState(true);
    model === null || model === void 0 ? void 0 : model.on("sort-X", () => setSortAsce(!sortAsce));
    const [cache] = hooks_2.useModelState("cache");
    const orient = JSON.parse(cache.includes("chartState") ? cache : `{"chartState":{"orient":"vertical"}}`).chartState.orient;
    const selectedCol = JSON.parse(cache.includes("selectedCol")
        ?
            cache
        :
            `{"selectedCol":[{"seriesName":"", "colName":"","chartType":"line", "yAxis":"left"}]}`).selectedCol;
    const leftCols = selectedCol.filter((item) => { return (item.yAxis === "left"); }).map((item) => item.colName);
    const rightCols = selectedCol.filter((item) => { return (item.yAxis === "right"); }).map((item) => item.colName);
    const yAxisList = (leftCols.length > 0 && rightCols.length > 0) ?
        ["y", "y2"]
        :
            leftCols.length > 0 ?
                ["y"]
                :
                    ["y2"];
    const charts = {
        "encoding": {
            "x": {
                field: orient === "vertical" ? XAxis : "y",
                axis: { labelAngle: 45 },
                sort: sortAsce ? "ascending" : "descending",
                type: orient === "vertical" ?
                    XAxis === "Index" ?
                        "quantitative"
                        :
                            dateColName.includes(XAxis) ?
                                "temporal"
                                :
                                    "nominal"
                    :
                        XAxis === "Index" ?
                            "quantitative"
                            :
                                "nominal"
            },
            "tooltip": [
                { "field": "x", "type": "nominal" }
            ]
        },
        "layer": yAxisList.map((item, index) => {
            return ({
                "transform": item === "y"
                    ?
                        [
                            {
                                "filter": {
                                    "field": "type",
                                    "oneOf": leftCols
                                }
                            }
                        ]
                    :
                        [
                            {
                                "filter": {
                                    "field": "type",
                                    "oneOf": rightCols
                                }
                            }
                        ],
                "encoding": {
                    y: {
                        field: orient === "vertical" ? "y" : XAxis,
                        type: orient === "vertical" ? "quantitative" : "nominal",
                        axis: {
                            orient: item === "y" ? "left" : "right"
                        }
                    },
                    opacity: {
                        condition: {
                            param: `hover_${index}`,
                            value: 0.8
                        },
                        value: 0.2
                    },
                },
                layer: [
                    // Chart type of visualization
                    ...selectedCol
                        .filter((series) => series.chartType !== "arc")
                        .map((series) => {
                        var _a;
                        return ({
                            mark: series.chartType,
                            transform: [
                                { "filter": `datum.type==='${series.colName}'` },
                                { "calculate": `datum.type + "_${(_a = series.chartType) !== null && _a !== void 0 ? _a : ""}"`, "as": "Legend" }
                            ],
                            "encoding": {
                                color: {
                                    condition: {
                                        param: `hover_${index}`,
                                        field: "Legend",
                                        type: "nominal",
                                    },
                                    value: "grey"
                                }
                            }
                        });
                    }),
                    // Hidden layer for interaction
                    {
                        params: [{
                                name: `hover_${index}`,
                                select: {
                                    type: "point",
                                    field: "Legend",
                                    on: "mouseover"
                                }
                            }],
                        mark: { type: "line", strokeWidth: 8, stroke: "transparent" }
                    },
                ]
            });
        })
    };
    const pieCharts = selectedCol
        .filter((series) => series.chartType === "arc")
        .map((series) => {
        return ({
            mark: { "type": "arc", "tooltip": true },
            transform: [
                { "filter": `datum.type==='${series.colName}'` }
            ],
            encoding: {
                "theta": { "field": "Theta", "aggregate": "count", "type": "quantitative" },
                "color": { "field": "Categories", "type": "nominal" },
                "tooltip": [
                    { "field": "Theta", "aggregate": "count", "type": "nominal" }
                ]
            }
        });
    });
    const hasPieChart = selectedCol.filter((series) => series.chartType === "arc").length > 0;
    const hasOtherCharts = selectedCol.filter((series) => series.chartType !== "arc").length > 0;
    const chartSpec = hasPieChart && hasOtherCharts ?
        {
            "hconcat": [
                charts,
                ...pieCharts
            ]
        }
        :
            hasPieChart ?
                { "hconcat": [...pieCharts] }
                : Object.assign({}, charts);
    const spec = Object.assign(Object.assign({ "$schema": "https://vega.github.io/schema/vega-lite/v5.json", "description": "Google's stock price over time.", "width": open ? rect.width - const_1.MenuWidth - const_1.LabelWidth : rect.width - 4 - const_1.LabelWidth, "height": const_1.ViewHeight, "transform": [
            {
                "calculate": XAxis === "Index" ?
                    "toNumber(datum.x)"
                    :
                        dateColName.includes(XAxis) ?
                            "datetime(datum.x)"
                            :
                                "datum.x",
                "as": XAxis,
            },
            {
                "calculate": `datum.type`, "as": "Label",
            },
            {
                "calculate": "datum.y", "as": "Theta"
            },
            {
                "calculate": "datum.x", "as": "Categories"
            }
        ], "data": { "values": lineData.values } }, chartSpec), { resolve: {
            scale: { "y": "independent" },
            legend: {
            // "color": "independent",
            // "size": "independent"
            }
        } });
    react_1.useEffect(() => {
        var view = new vega_embed_1.vega.View(vega_embed_1.vega.parse(vega_embed_1.vegaLite.compile(spec).spec), { renderer: 'none' });
        view
            .toCanvas()
            .then(png => {
            var base64Image = png.toDataURL();
            const decode = decodeURIComponent(base64Image);
            model === null || model === void 0 ? void 0 : model.set("png", decode.substring(22, decode.length));
            model === null || model === void 0 ? void 0 : model.save_changes();
        })
            .catch(error => {
            console.error('Error rendering chart:', error);
        });
    }, [lineData]);
    return (react_1.default.createElement(react_vega_1.VegaLite, { renderer: 'svg', actions: false, spec: spec }));
};
const Visualization = () => {
    const model = hooks_2.useModel();
    const cache = model === null || model === void 0 ? void 0 : model.get("cache");
    const [XAxis, setXAxis] = react_1.useState(JSON.parse(cache.includes("xAxisState") && !cache.includes(`{"xAxisState":""}`) ? cache : `{"xAxisState":"Index"}`)["xAxisState"]);
    const [ref, rect] = hooks_1.useResizeObserver();
    const [open, setOpen] = react_1.useState(true);
    return (react_1.default.createElement(core_1.Group, { grow: true, ref: ref, sx: { margin: "auto 1rem auto 0rem" } },
        react_1.default.createElement(core_1.Group, { noWrap: true, sx: { height: "100%", marginTop: "1rem", gap: "0", alignItems: "flex-start", justifyContent: "space-between" } },
            react_1.default.createElement(core_1.Group, { noWrap: true, sx: { gap: "0", width: "16rem" } }, open ?
                react_1.default.createElement(menu_1.VisualMenu, { XAxis: XAxis, setXAxis: setXAxis })
                :
                    react_1.default.createElement(react_1.default.Fragment, null)),
            react_1.default.createElement(core_1.ActionIcon, { onClick: () => { setOpen(!open); } }, open ?
                react_1.default.createElement(icons_react_1.IconChevronLeft, null)
                :
                    react_1.default.createElement(icons_react_1.IconChevronRight, null)),
            react_1.default.createElement(core_1.Divider, { orientation: "vertical" }),
            react_1.default.createElement(core_1.Group, { w: open ? rect.width - 256 - 28 : rect.width - 28 },
                react_1.default.createElement(VisualPreviewChart, { rect: rect, XAxis: XAxis, open: open })))));
};
exports.Visualization = Visualization;
//# sourceMappingURL=visualization.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".custom-widget {\n  padding: 0px 2px;\n}\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"asqlcell","version":"0.1.0","description":"Analytical sql cell for Jupyter","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/datarho/asqlcell","bugs":{"url":"https://github.com/datarho/asqlcell/issues"},"license":"BSD-3-Clause","author":{"name":"qizh","email":"qizh@datarho.tech"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/datarho/asqlcell"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf asqlcell/labextension","clean:nbextension":"rimraf asqlcell/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@emotion/react":"^11.10.5","@emotion/serialize":"^1.1.1","@emotion/utils":"^1.2.0","@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","@mantine/core":"^5.10.0","@mantine/hooks":"^5.10.0","@tabler/icons-react":"^2.14.0","react":"^18.2.0","react-dom":"^17.0.2","react-icons":"^4.7.1","react-vega":"^7.6.0","vega":"^5.22.1","vega-embed":"^6.22.1","vega-lite":"^5.6.0"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@babel/preset-react":"^7.14.5","@babel/preset-typescript":"^7.14.5","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/react":"^17.0.11","@types/react-dom":"^17.0.8","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","babel-loader":"^8.2.2","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-plugin-react":"^7.31.11","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","jest-canvas-mock":"^2.4.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"babel":{"presets":["@babel/preset-env","@babel/preset-react","@babel/preset-typescript"]},"jupyterlab":{"extension":"lib/plugin","outputDir":"asqlcell/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_WidgetModel_js.495a0bc8f6fafed938d1.js.map