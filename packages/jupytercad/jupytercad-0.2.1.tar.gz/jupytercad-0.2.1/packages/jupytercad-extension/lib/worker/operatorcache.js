import { hashCode } from './utils';
const SHAPE_CACHE = new Map();
const PRIMITIVE_OPERATORS = [
    'Part::Box',
    'Part::Cylinder',
    'Part::Sphere',
    'Part::Cone',
    'Part::Torus'
];
const BOOLEAN_OPERATORS = [
    'Part::Cut',
    'Part::MultiFuse',
    'Part::Extrusion',
    'Part::MultiCommon'
];
const MISC_OPERATORS = ['BrepFile', 'Sketcher::SketchObject'];
export function expand_operator(name, args, content) {
    const expanded_args = {};
    if (PRIMITIVE_OPERATORS.includes(name)) {
        expanded_args[name] = args;
    }
    else if (BOOLEAN_OPERATORS.includes(name)) {
        switch (name) {
            case 'Part::Cut': {
                const expandedArgs = JSON.parse(JSON.stringify(args));
                const { Base, Tool } = expandedArgs;
                const baseData = content.objects.filter(item => item.name === Base);
                const toolData = content.objects.filter(item => item.name === Tool);
                if (baseData.length > 0) {
                    expandedArgs.Base = expand_operator(baseData[0].shape, baseData[0].parameters, content);
                }
                if (toolData.length > 0) {
                    expandedArgs.Tool = expand_operator(toolData[0].shape, toolData[0].parameters, content);
                }
                expanded_args[name] = expandedArgs;
                break;
            }
            case 'Part::Extrusion': {
                const expandedArgs = JSON.parse(JSON.stringify(args));
                const { Base } = expandedArgs;
                const baseData = content.objects.filter(item => item.name === Base);
                if (baseData.length > 0) {
                    expandedArgs.Base = expand_operator(baseData[0].shape, baseData[0].parameters, content);
                }
                expanded_args[name] = expandedArgs;
                break;
            }
            case 'Part::MultiCommon':
            case 'Part::MultiFuse': {
                const expandedArgs = JSON.parse(JSON.stringify(args));
                const { Shapes } = expandedArgs;
                const newShapes = [];
                Shapes.forEach(element => {
                    const elementData = content.objects.filter(item => item.name === element);
                    if (elementData.length > 0) {
                        newShapes.push(expand_operator(elementData[0].shape, elementData[0].parameters, content));
                    }
                });
                expandedArgs.Shapes = newShapes;
                expanded_args[name] = expandedArgs;
                break;
            }
            default:
                break;
        }
    }
    else if (MISC_OPERATORS.includes(name)) {
        expanded_args[name] = args;
    }
    else {
        expanded_args[name] = args;
    }
    return expanded_args;
}
export function operatorCache(name, ops) {
    return (args, content) => {
        const expandedArgs = expand_operator(name, args, content);
        const hash = `${hashCode(JSON.stringify(expandedArgs))}`;
        if (SHAPE_CACHE.has(hash)) {
            return SHAPE_CACHE.get(hash);
        }
        else {
            const shape = ops(args, content);
            if (shape) {
                SHAPE_CACHE.set(hash, shape);
            }
            return shape;
        }
    };
}
