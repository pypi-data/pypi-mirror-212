import { DataType } from '../datatypes';
import { Lens } from './types';
export type LensKey = string;
interface Registry {
    views: Record<LensKey, Lens>;
    keys: string[];
    findCompatibleViews(types: DataType[], canEdit: boolean): string[];
    register(lens: Lens): void;
}
export declare function isLensCompatible(view: Lens, types: DataType[], canEdit: boolean): boolean;
declare const registry: Registry;
export default registry;
