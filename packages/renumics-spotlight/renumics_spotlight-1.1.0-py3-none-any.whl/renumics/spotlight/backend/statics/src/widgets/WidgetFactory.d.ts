import * as React from 'react';
import { Config, Widget } from './types';
interface Props {
    widgetType: string;
    widgetId: string;
    config: Record<string, unknown>;
    setConfig: React.Dispatch<React.SetStateAction<Config>>;
}
export declare const widgets: Widget[];
export declare const widgetsById: Record<string, Widget>;
declare const _default: React.NamedExoticComponent<Props>;
export default _default;
