

TestStringComponent = createScinodeComponent({"name": "TestString", "catalog": "Test", "controls": [["Int", "t"], ["String", "String"]], "inputs": [], "outputs": [["String", "String"]]});
TestFloatComponent = createScinodeComponent({"name": "TestFloat", "catalog": "Test", "controls": [["Int", "t"], ["Float", "Float"]], "inputs": [], "outputs": [["Float", "Float"]]});
TestAddComponent = createScinodeComponent({"name": "TestAdd", "catalog": "Test", "controls": [["Int", "t"]], "inputs": [["Float", "x"], ["Float", "y"]], "outputs": [["Float", "Result"]]});
TestMinusComponent = createScinodeComponent({"name": "TestMinus", "catalog": "Test", "controls": [["Int", "t"]], "inputs": [["Float", "x"], ["Float", "y"]], "outputs": [["Float", "Result"]]});
TestSqrtComponent = createScinodeComponent({"name": "TestSqrt", "catalog": "Test", "controls": [["Int", "t"]], "inputs": [["Float", "x"]], "outputs": [["Float", "Result"]]});
TestGreaterComponent = createScinodeComponent({"name": "TestGreater", "catalog": "Test", "controls": [["Int", "t"]], "inputs": [["Float", "x"], ["Float", "y"]], "outputs": [["Bool", "Result"]]});
TestLessComponent = createScinodeComponent({"name": "TestLess", "catalog": "Test", "controls": [["Int", "t"]], "inputs": [["Float", "x"], ["Float", "y"]], "outputs": [["Bool", "Result"]]});
TestRangeComponent = createScinodeComponent({"name": "TestRange", "catalog": "Test", "controls": [["Float", "start"], ["Float", "stop"], ["Float", "step"]], "inputs": [], "outputs": [["Float", "Result"]]});
TestEnumComponent = createScinodeComponent({"name": "TestEnum", "catalog": "Test", "controls": [["Int", "t"], ["Enum", "function", {"options": ["add", "sqrt"], "defaultVal": "add"}]], "inputs": [["Float", "x"], ["Float", "y"]], "outputs": [["Float", "Result"]]});



class TestEnumUpdateComponent extends ScinodeComponent {
    constructor(){
        super("TestEnumUpdate");
        this.catalog = 'Test';
        this.name = 'TestEnumUpdate'
    }

    createControls(node, callback) {
        node.addControl(new IntControl(this.editor, 't'));
        var ctl1 = new EnumUpdateControl(this.editor, 'function',
                    {"options": ['add', 'sqrt'], "defaultVal": "add"},
                    callback);
        node.addControl(ctl1);
    }

    createSockets(node){
        if (node.data['function'] == undefined || node.data['function'] == 'add') {
            var inp1 = new Rete.Input('x', "x", SocketFloat);
            var inp2 = new Rete.Input('y', "y", SocketFloat);
            var out = new Rete.Output('Result', "Result", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'x'))
            inp2.addControl(new FloatControl(editor, 'y'))
            node.addInput(inp1)
                .addInput(inp2)
                .addOutput(out);
        }
        else {
            var inp1 = new Rete.Input('x', "x", SocketFloat);
            var out = new Rete.Output('Result', "Result", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'x'))
            node.addInput(inp1)
                .addOutput(out);
        }
    }

    builder(node) {
        function setControls(node) {
            // control, for the enum control with callback
            console.log("data: ", node.data)
            console.log("setControls: ", node.name)
            for ( let [key, control] of node.controls) {
                if (node.data[key] != undefined) {
                    console.log("control: ", key, node.data[key]);
                    control.setValue(node.data[key]);
                }
            }
        };
        async function callback() {
            node.inputs.forEach(function(input, key) {
                // delete data from input control
                delete node.data[input.name];
                // remote the connection
                for (let i = 0; i < input.connections.length; i++) {
                    input.connections[i].remove();
                }
                node.removeInput(input);
            })
            node.outputs.forEach(function(output, key) {
                // remote the connection
                for (let i = 0; i < output.connections.length; i++) {
                    output.connections[i].remove();
                }
                node.removeOutput(output);
            })
            await node.update();
            if (node.data['function'] == 'add') {
                var inp1 = new Rete.Input('x', "x", SocketFloat);
                var inp2 = new Rete.Input('y', "y", SocketFloat);
                var out = new Rete.Output('Result', "Result", SocketFloat);
                inp1.addControl(new FloatControl(editor, 'x'))
                inp2.addControl(new FloatControl(editor, 'y'))
                node.addInput(inp1)
                    .addInput(inp2)
                    .addOutput(out);
            }
            else {
                var inp1 = new Rete.Input('x', "x", SocketFloat);
                var out = new Rete.Output('Result', "Result", SocketFloat);
                inp1.addControl(new FloatControl(editor, 'x'))
                node.addInput(inp1)
                    .addOutput(out);
            }
        await node.update();
        setTimeout( () => { this.emitter.view.updateConnections({node}); }, 10);
        };

        this.init(node);
        console.log("data: t", node.data['t'])
        this.createControls(node, callback);
        this.createSockets(node);
        // setControls(node);
        return node
    }
}


// Numpy


var func_items = ["DataSource", "MachAr", "Tester", "abs", "absolute", "add", "add_docstring", "add_newdoc", "add_newdoc_ufunc", "alen", "all", "allclose", "alltrue", "amax", "amin", "angle", "any", "append", "apply_along_axis", "apply_over_axes", "arange", "arccos", "arccosh", "arcsin", "arcsinh", "arctan", "arctan2", "arctanh", "argmax", "argmin", "argpartition", "argsort", "argwhere", "around", "array", "array2string", "array_equal", "array_equiv", "array_repr", "array_split", "array_str", "asanyarray", "asarray", "asarray_chkfinite", "ascontiguousarray", "asfarray", "asfortranarray", "asmatrix", "asscalar", "atleast_1d", "atleast_2d", "atleast_3d", "average", "bartlett", "base_repr", "binary_repr", "bincount", "bitwise_and", "bitwise_not", "bitwise_or", "bitwise_xor", "blackman", "block", "bmat", "bool", "bool8", "bool_", "broadcast", "broadcast_arrays", "broadcast_to", "busday_count", "busday_offset", "busdaycalendar", "byte", "byte_bounds", "bytes0", "bytes_", "can_cast", "cbrt", "cdouble", "ceil", "cfloat", "character", "chararray", "choose", "clip", "clongdouble", "clongfloat", "column_stack", "common_type", "compare_chararrays", "complex", "complex128", "complex256", "complex64", "complex_", "complexfloating", "compress", "concatenate", "conj", "conjugate", "convolve", "copy", "copysign", "copyto", "corrcoef", "correlate", "cos", "cosh", "count_nonzero", "cov", "cross", "csingle", "cumprod", "cumproduct", "cumsum", "datetime64", "datetime_as_string", "datetime_data", "deg2rad", "degrees", "delete", "deprecate", "deprecate_with_doc", "diag", "diag_indices", "diag_indices_from", "diagflat", "diagonal", "diff", "digitize", "disp", "divide", "divmod", "dot", "double", "dsplit", "dstack", "dtype", "ediff1d", "einsum", "einsum_path", "empty", "empty_like", "equal", "errstate", "exp", "exp2", "expand_dims", "expm1", "extract", "eye", "fabs", "fastCopyAndTranspose", "fill_diagonal", "find_common_type", "finfo", "fix", "flatiter", "flatnonzero", "flexible", "flip", "fliplr", "flipud", "float", "float128", "float16", "float32", "float64", "float_", "float_power", "floating", "floor", "floor_divide", "fmax", "fmin", "fmod", "format_float_positional", "format_float_scientific", "format_parser", "frexp", "frombuffer", "fromfile", "fromfunction", "fromiter", "frompyfunc", "fromregex", "fromstring", "full", "full_like", "fv", "gcd", "generic", "genfromtxt", "geomspace", "get_array_wrap", "get_include", "get_printoptions", "getbufsize", "geterr", "geterrcall", "geterrobj", "gradient", "greater", "greater_equal", "half", "hamming", "hanning", "heaviside", "histogram", "histogram2d", "histogram_bin_edges", "histogramdd", "hsplit", "hstack", "hypot", "i0", "identity", "iinfo", "imag", "in1d", "indices", "inexact", "info", "inner", "insert", "int", "int0", "int16", "int32", "int64", "int8", "int_", "intc", "integer", "interp", "intersect1d", "intp", "invert", "ipmt", "irr", "is_busday", "isclose", "iscomplex", "iscomplexobj", "isfinite", "isfortran", "isin", "isinf", "isnan", "isnat", "isneginf", "isposinf", "isreal", "isrealobj", "isscalar", "issctype", "issubclass_", "issubdtype", "issubsctype", "iterable", "ix_", "kaiser", "kron", "lcm", "ldexp", "left_shift", "less", "less_equal", "lexsort", "linspace", "load", "loads", "loadtxt", "log", "log10", "log1p", "log2", "logaddexp", "logaddexp2", "logical_and", "logical_not", "logical_or", "logical_xor", "logspace", "long", "longcomplex", "longdouble", "longfloat", "longlong", "lookfor", "mafromtxt", "mask_indices", "mat", "matmul", "matrix", "max", "maximum", "maximum_sctype", "may_share_memory", "mean", "median", "memmap", "meshgrid", "min", "min_scalar_type", "minimum", "mintypecode", "mirr", "mod", "modf", "moveaxis", "msort", "multiply", "nan_to_num", "nanargmax", "nanargmin", "nancumprod", "nancumsum", "nanmax", "nanmean", "nanmedian", "nanmin", "nanpercentile", "nanprod", "nanquantile", "nanstd", "nansum", "nanvar", "ndarray", "ndenumerate", "ndfromtxt", "ndim", "ndindex", "nditer", "negative", "nested_iters", "nextafter", "nonzero", "not_equal", "nper", "npv", "number", "obj2sctype", "object", "object0", "object_", "ones", "ones_like", "outer", "packbits", "pad", "partition", "percentile", "piecewise", "place", "pmt", "poly", "poly1d", "polyadd", "polyder", "polydiv", "polyfit", "polyint", "polymul", "polysub", "polyval", "positive", "power", "ppmt", "printoptions", "prod", "product", "promote_types", "ptp", "put", "put_along_axis", "putmask", "pv", "quantile", "rad2deg", "radians", "rate", "ravel", "ravel_multi_index", "real", "real_if_close", "recarray", "recfromcsv", "recfromtxt", "reciprocal", "record", "remainder", "repeat", "require", "reshape", "resize", "result_type", "right_shift", "rint", "roll", "rollaxis", "roots", "rot90", "round", "round_", "row_stack", "safe_eval", "save", "savetxt", "savez", "savez_compressed", "sctype2char", "searchsorted", "select", "set_numeric_ops", "set_printoptions", "set_string_function", "setbufsize", "setdiff1d", "seterr", "seterrcall", "seterrobj", "setxor1d", "shape", "shares_memory", "short", "show_config", "sign", "signbit", "signedinteger", "sin", "sinc", "single", "singlecomplex", "sinh", "size", "sometrue", "sort", "sort_complex", "source", "spacing", "split", "sqrt", "square", "squeeze", "stack", "std", "str", "str0", "str_", "string_", "subtract", "sum", "swapaxes", "take", "take_along_axis", "tan", "tanh", "tensordot", "test", "tile", "timedelta64", "trace", "transpose", "trapz", "tri", "tril", "tril_indices", "tril_indices_from", "trim_zeros", "triu", "triu_indices", "triu_indices_from", "true_divide", "trunc", "typename", "ubyte", "ufunc", "uint", "uint0", "uint16", "uint32", "uint64", "uint8", "uintc", "uintp", "ulonglong", "unicode", "unicode_", "union1d", "unique", "unpackbits", "unravel_index", "unsignedinteger", "unwrap", "ushort", "vander", "var", "vdot", "vectorize", "void", "void0", "vsplit", "vstack", "where", "who", "zeros", "zeros_like"];

class NumpyComponent extends ScinodeComponent {
    constructor(){
        super("Numpy");
        this.catalog = 'Math';
        this.name = 'Numpy'
    }

    createControls(node, callback) {
        var ctl1 = new EnumUpdateControl(this.editor, 'function',
                    {"options": func_items, "defaultVal": "add"},
                    callback);
        node.addControl(ctl1);
    }

    createSockets(node){
        if (node.data['function'] == undefined || [
            "multiply",
            "divide",
            "power",
            "substract",
            "mod",
            "greater",
            "less",
            "add",
        ].includes(node.data['function'])) {
            var inp1 = new Rete.Input('x1', "x1", SocketFloat);
            var inp2 = new Rete.Input('x2', "x2", SocketFloat);
            var out = new Rete.Output('Result', "Result", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'x1'))
            inp2.addControl(new FloatControl(editor, 'x2'))
            node.addInput(inp1)
                .addInput(inp2)
                .addOutput(out);
        }
        else if (["linspace"].includes(node.data['function'])) {
            var inp1 = new Rete.Input('start', "start", SocketFloat);
            var inp2 = new Rete.Input('stop', "stop", SocketFloat);
            var inp3 = new Rete.Input('num', "num", SocketFloat);
            var out = new Rete.Output('Result', "Result", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'start'))
            inp2.addControl(new FloatControl(editor, 'stop'))
            inp3.addControl(new FloatControl(editor, 'num'))
            node.addInput(inp1)
                .addInput(inp2)
                .addInput(inp3)
                .addOutput(out);
        }
        else if (["arange"].includes(node.data['function'])) {
            var inp1 = new Rete.Input('start', "start", SocketFloat);
            var inp2 = new Rete.Input('stop', "stop", SocketFloat);
            var inp3 = new Rete.Input('step', "step", SocketFloat);
            var out = new Rete.Output('Result', "Result", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'start'))
            inp2.addControl(new FloatControl(editor, 'stop'))
            inp3.addControl(new FloatControl(editor, 'step'))
            node.addInput(inp1)
                .addInput(inp2)
                .addInput(inp3)
                .addOutput(out);
        }
        else if (["cos", "sin"].includes(node.data['function'])) {
            var inp1 = new Rete.Input('x', "x", SocketFloat);
            var out = new Rete.Output('Result', "Result", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'x'))
            node.addInput(inp1)
                .addOutput(out);
        }
        else if (["argmax", "argmin"].includes(node.data['function'])) {
            var inp1 = new Rete.Input('a', "a", SocketGeneral);
            var inp2 = new Rete.Input('axis', "axis", SocketFloat);
            var out = new Rete.Output('Result', "Result", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'x'))
            node.addInput(inp1)
                .addInput(inp2)
                .addOutput(out);
        }
        else {
            var inp1 = new Rete.Input('x', "x", SocketFloat);
            var out = new Rete.Output('Result', "Result", SocketFloat);
            inp1.addControl(new FloatControl(editor, 'x'))
            node.addInput(inp1)
                .addOutput(out);
        }
    }

    builder(node) {
        function setControls(node) {
            // control, for the enum control with callback
            for ( let [key, control] of node.controls) {
                if (node.data[key] != undefined) {
                    console.log("control: ", key, node.data[key]);
                    control.setValue(node.data[key]);
                }
            }
        };
        async function callback() {
            node.inputs.forEach(function(input, key) {
                // delete data from input control
                delete node.data[input.name];
                // remote the connection
                for (let i = 0; i < input.connections.length; i++) {
                    input.connections[i].remove();
                }
                node.removeInput(input);
            })
            node.outputs.forEach(function(output, key) {
                // remote the connection
                for (let i = 0; i < output.connections.length; i++) {
                    output.connections[i].remove();
                }
                node.removeOutput(output);
            })
            await node.update();
            if (node.data['function'] == 'add') {
                var inp1 = new Rete.Input('x', "x", SocketFloat);
                var inp2 = new Rete.Input('y', "y", SocketFloat);
                var out = new Rete.Output('Result', "Result", SocketFloat);
                inp1.addControl(new FloatControl(editor, 'x'))
                inp2.addControl(new FloatControl(editor, 'y'))
                node.addInput(inp1)
                    .addInput(inp2)
                    .addOutput(out);
            }
            else {
                var inp1 = new Rete.Input('x', "x", SocketFloat);
                var out = new Rete.Output('Result', "Result", SocketFloat);
                inp1.addControl(new FloatControl(editor, 'x'))
                node.addInput(inp1)
                    .addOutput(out);
            }
        await node.update();
        setTimeout( () => { this.emitter.view.updateConnections({node}); }, 10);
        };

        this.init(node);
        this.createControls(node, callback);
        this.createSockets(node);
        // setControls(node);
        return node
    }
}


// python builtin
StringComponent = createScinodeComponent({"name": "String", "catalog": "Input", "controls": [["String", "String"]], "inputs": [], "outputs": [["String", "String"]]});
IntComponent = createScinodeComponent({"name": "Int", "catalog": "Input", "controls": [["Int", "Int"]], "inputs": [], "outputs": [["Int", "Int"]]});
FloatComponent = createScinodeComponent({"name": "Float", "catalog": "Input", "controls": [["Float", "Float"]], "inputs": [], "outputs": [["Float", "Float"]]});
BoolComponent = createScinodeComponent({"name": "Bool", "catalog": "Input", "controls": [["Bool", "Bool"]], "inputs": [], "outputs": [["Bool", "Bool"]]});
GetattrComponent = createScinodeComponent({"name": "Getattr", "catalog": "Utils", "controls": [], "inputs": [["General", "Source"], ["String", "Name", {"String": "Name"}]], "outputs": [["General", "Result"]]});
SetattrComponent = createScinodeComponent({"name": "Setattr", "catalog": "Utils", "controls": [], "inputs": [["General", "Source"], ["String", "Name", {"String": "Name"}], ["General", "Value"]], "outputs": [["General", "Result"]]});
GetitemComponent = createScinodeComponent({"name": "Getitem", "catalog": "Utils", "controls": [], "inputs": [["General", "Source"], ["General", "Index", {"Float": "Index"}]], "outputs": [["General", "Result"]]});
SetitemComponent = createScinodeComponent({"name": "Setitem", "catalog": "Utils", "controls": [], "inputs": [["General", "Source"], ["General", "Index", {"Float": "Index"}], ["General", "Value"]], "outputs": [["General", "Result"]]});
IndexComponent = createScinodeComponent({"name": "Index", "catalog": "Utils", "controls": [], "inputs": [["General", "Source"], ["General", "Value", {"Float": "Value"}]], "outputs": [["General", "Index"]]});
ScatterComponent = createScinodeComponent({"name": "Scatter", "catalog": "Control", "controls": [["String", "DataType", {"defaultVal": "General"}]], "inputs": [["General", "Input"], ["General", "Stop"]], "outputs": [["General", "Result"]]});
SwitchComponent = createScinodeComponent({"name": "Switch", "catalog": "Control", "controls": [], "inputs": [["General", "Input"], ["General", "Switch"]], "outputs": [["General", "Result"]]});
UpdateComponent = createScinodeComponent({"name": "Update", "catalog": "Control", "controls": [], "inputs": [["General", "Input"], ["General", "Update"]], "outputs": [["General", "Result"]]});


// Test
// TestNGLComponent = createScinodeComponent({"name": "TestNGL", "catalog": "Utils", "local": true, "controls": [["NGL", "Viewer"]], "inputs": [["String", "Atoms"]], "outputs": []});


class TestNGLComponent extends ScinodeComponent {

    constructor(){
        super("NGL");
        this.catalog = 'Test';
        this.name = "TestNGL";
        this.local=true;
    }

    builder(node) {
        this.init(node);
        node.addControl(new NGLControl(this.editor, 'Viewer', node));
        var inp1 = new Rete.Input('Atoms', "Atoms", SocketGeneral);
        return node.addInput(inp1);
    }
}

var components = [
    new TestStringComponent(),
    new TestFloatComponent(),
    new TestAddComponent(),
    new TestMinusComponent(),
    new TestSqrtComponent(),
    new TestGreaterComponent(),
    new TestLessComponent(),
    new TestRangeComponent(),
    new TestEnumComponent(),
    new TestEnumUpdateComponent(),
    // python builtin
    new StringComponent(),
    new IntComponent(),
    new FloatComponent(),
    new BoolComponent(),
    //
    new GetattrComponent(),
    new SetattrComponent(),
    new GetitemComponent(),
    new SetitemComponent(),
    new IndexComponent(),
    // control
    new ScatterComponent(),
    new SwitchComponent(),
    new UpdateComponent(),
    //
    new NumpyComponent(),
    // Test
    new TestNGLComponent(),
];

// register all nodes
components.map(c => {
    editor.register(c);
    engine.register(c);
    });
