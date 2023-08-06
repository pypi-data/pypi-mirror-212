import { FunctionComponent } from 'react';
import type { GridProps } from 'react-window';
interface Props {
    width: number;
    height: number;
    onScroll: GridProps['onScroll'];
}
declare const TableGrid: FunctionComponent<Props>;
export default TableGrid;
