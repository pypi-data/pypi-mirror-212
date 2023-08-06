import * as datatypes from './datatypes';
export interface DataColumn {
    order: number;
    index: number;
    name: string;
    type: datatypes.DataType;
    hidden?: boolean;
    lazy: boolean;
    editable: boolean;
    optional: boolean;
    isInternal: boolean;
    description?: string;
    key: string;
    tags?: string[];
}
export interface NumberColumn extends DataColumn {
    type: datatypes.NumericalDataType;
}
export declare const isNumberColumn: (col: DataColumn) => col is NumberColumn;
export interface BooleanColumn extends DataColumn {
    type: datatypes.BooleanDataType;
}
export declare const isBooleanColumn: (col: DataColumn) => col is BooleanColumn;
export interface CategoricalColumn extends DataColumn {
    type: datatypes.CategoricalDataType;
}
export declare const isCategoricalColumn: (col: DataColumn) => col is CategoricalColumn;
export interface ScalarColumn extends DataColumn {
    type: datatypes.ScalarDataType;
}
export declare const isScalarColumn: (col: DataColumn) => col is ScalarColumn;
export interface ArrayColumn extends DataColumn {
    type: datatypes.ScalarDataType;
}
export declare const isArrayColumn: (col: DataColumn) => col is ArrayColumn;
export interface EmbeddingColumn extends DataColumn {
    type: datatypes.EmbeddingDataType;
}
export declare const isEmbeddingColumn: (col: DataColumn) => col is EmbeddingColumn;
export interface DateColumn extends DataColumn {
    type: datatypes.DateTimeDataType;
}
export declare const isDateColumn: (col: DataColumn) => col is DateColumn;
export interface Sequence1DColumn extends DataColumn {
    type: datatypes.SequenceDataType;
    yLabel?: string;
    xLabel?: string;
}
export declare const isSequence1DColumn: (col: DataColumn) => col is Sequence1DColumn;
export interface MeshColumn extends DataColumn {
    type: datatypes.MeshDataType;
}
export declare const isMeshColumn: (col: DataColumn) => col is MeshColumn;
export interface ImageColumn extends DataColumn {
    type: datatypes.ImageDataType;
}
export declare const isImageColumn: (col: DataColumn) => col is ImageColumn;
export interface UnknownColumn extends DataColumn {
    type: datatypes.UnknownDataType;
}
export declare const isUnknownColumn: (col: DataColumn) => col is UnknownColumn;
export interface RowValues {
    [key: string]: any;
}
export interface DataRow {
    index: number;
    values: RowValues;
}
export type ColumnData = any[] | Int32Array | Float32Array;
export type TableData = Record<string, ColumnData>;
export interface DataStatistics {
    max: number;
    min: number;
    mean: number;
    p95: number;
    p5: number;
    std: number;
}
export type ColumnsStats = Record<string, DataStatistics | undefined>;
export interface DataFrame {
    columns: DataColumn[];
    length: number;
    data: TableData;
}
export interface Predicate<T = any> {
    shorthand: string;
    compare: (value: any, referenceValue: T) => boolean;
}
export declare abstract class Filter {
    kind: string;
    isEnabled: boolean;
    isInverted: boolean;
    abstract apply(rowIndex: number, data: TableData): boolean;
}
export declare class PredicateFilter<T = any> extends Filter {
    kind: 'PredicateFilter';
    column: DataColumn;
    predicate: Predicate<T>;
    referenceValue: T;
    constructor(column: DataColumn, predicate: Predicate<T>, referenceValue: T);
    get type(): datatypes.DataType;
    apply(rowIndex: number, data: TableData): boolean;
}
export declare class SetFilter extends Filter {
    kind: 'SetFilter';
    rowIndices: Set<number>;
    name: string;
    constructor(rows: number[] | Set<number>, name?: string);
    static fromMask(mask: boolean[], name?: string): SetFilter;
    apply(rowIndex: number): boolean;
}
export type TableView = 'full' | 'filtered' | 'selected';
export type Vec2 = [number, number];
export interface Problem {
    type: string;
    title: string;
    detail?: string;
    instance?: string;
}
export type IndexArray = number[] | Int32Array;
export type TypedArray = Int8Array | Uint8Array | Int16Array | Uint16Array | Int32Array | Uint32Array | Uint8ClampedArray | Float32Array | Float64Array;
export interface BaseLayoutNode {
    kind: string;
}
export interface SplitNode extends BaseLayoutNode {
    kind: 'split';
    weight: number;
    orientation?: 'horizontal' | 'vertical';
    children: ContainerNode[];
}
export interface WidgetNode extends BaseLayoutNode {
    kind: 'widget';
    type: string;
    name?: string;
    config?: Record<string, unknown>;
}
export interface TabNode extends BaseLayoutNode {
    kind: 'tab';
    weight: number;
    children: WidgetNode[];
}
export type ContainerNode = SplitNode | TabNode;
export type LayoutNode = ContainerNode | WidgetNode;
export interface AppLayout {
    orientation?: 'horizontal' | 'vertical';
    children: ContainerNode[];
}
