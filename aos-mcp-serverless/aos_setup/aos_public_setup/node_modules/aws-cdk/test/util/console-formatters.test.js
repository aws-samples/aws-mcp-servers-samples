"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
/* eslint-disable import/order */
const chalk = require("chalk");
const console_formatters_1 = require("../../lib/util/console-formatters");
test('no banner on empty msg list', () => expect((0, console_formatters_1.formatAsBanner)([])).toEqual([]));
test('banner works as expected', () => expect((0, console_formatters_1.formatAsBanner)(['msg1', 'msg2'])).toEqual([
    '************',
    '*** msg1 ***',
    '*** msg2 ***',
    '************',
]));
test('banner works for formatted msgs', () => expect((0, console_formatters_1.formatAsBanner)([
    'hello msg1',
    chalk.yellow('hello msg2'),
    chalk.bold('hello msg3'),
])).toEqual([
    '******************',
    '*** hello msg1 ***',
    `*** ${chalk.yellow('hello msg2')} ***`,
    `*** ${chalk.bold('hello msg3')} ***`,
    '******************',
]));
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiY29uc29sZS1mb3JtYXR0ZXJzLnRlc3QuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyJjb25zb2xlLWZvcm1hdHRlcnMudGVzdC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOztBQUFBLGlDQUFpQztBQUNqQywrQkFBK0I7QUFDL0IsMEVBQW1FO0FBRW5FLElBQUksQ0FBQyw2QkFBNkIsRUFBRSxHQUFHLEVBQUUsQ0FDdkMsTUFBTSxDQUFDLElBQUEsbUNBQWMsRUFBQyxFQUFFLENBQUMsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxFQUFFLENBQUMsQ0FBQyxDQUFDO0FBRTFDLElBQUksQ0FBQywwQkFBMEIsRUFBRSxHQUFHLEVBQUUsQ0FDcEMsTUFBTSxDQUFDLElBQUEsbUNBQWMsRUFBQyxDQUFDLE1BQU0sRUFBRSxNQUFNLENBQUMsQ0FBQyxDQUFDLENBQUMsT0FBTyxDQUFDO0lBQy9DLGNBQWM7SUFDZCxjQUFjO0lBQ2QsY0FBYztJQUNkLGNBQWM7Q0FDZixDQUFDLENBQUMsQ0FBQztBQUVOLElBQUksQ0FBQyxpQ0FBaUMsRUFBRSxHQUFHLEVBQUUsQ0FDM0MsTUFBTSxDQUFDLElBQUEsbUNBQWMsRUFBQztJQUNwQixZQUFZO0lBQ1osS0FBSyxDQUFDLE1BQU0sQ0FBQyxZQUFZLENBQUM7SUFDMUIsS0FBSyxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUM7Q0FDekIsQ0FBQyxDQUFDLENBQUMsT0FBTyxDQUFDO0lBQ1Ysb0JBQW9CO0lBQ3BCLG9CQUFvQjtJQUNwQixPQUFPLEtBQUssQ0FBQyxNQUFNLENBQUMsWUFBWSxDQUFDLE1BQU07SUFDdkMsT0FBTyxLQUFLLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxNQUFNO0lBQ3JDLG9CQUFvQjtDQUNyQixDQUFDLENBQUMsQ0FBQyIsInNvdXJjZXNDb250ZW50IjpbIi8qIGVzbGludC1kaXNhYmxlIGltcG9ydC9vcmRlciAqL1xuaW1wb3J0ICogYXMgY2hhbGsgZnJvbSAnY2hhbGsnO1xuaW1wb3J0IHsgZm9ybWF0QXNCYW5uZXIgfSBmcm9tICcuLi8uLi9saWIvdXRpbC9jb25zb2xlLWZvcm1hdHRlcnMnO1xuXG50ZXN0KCdubyBiYW5uZXIgb24gZW1wdHkgbXNnIGxpc3QnLCAoKSA9PlxuICBleHBlY3QoZm9ybWF0QXNCYW5uZXIoW10pKS50b0VxdWFsKFtdKSk7XG5cbnRlc3QoJ2Jhbm5lciB3b3JrcyBhcyBleHBlY3RlZCcsICgpID0+XG4gIGV4cGVjdChmb3JtYXRBc0Jhbm5lcihbJ21zZzEnLCAnbXNnMiddKSkudG9FcXVhbChbXG4gICAgJyoqKioqKioqKioqKicsXG4gICAgJyoqKiBtc2cxICoqKicsXG4gICAgJyoqKiBtc2cyICoqKicsXG4gICAgJyoqKioqKioqKioqKicsXG4gIF0pKTtcblxudGVzdCgnYmFubmVyIHdvcmtzIGZvciBmb3JtYXR0ZWQgbXNncycsICgpID0+XG4gIGV4cGVjdChmb3JtYXRBc0Jhbm5lcihbXG4gICAgJ2hlbGxvIG1zZzEnLFxuICAgIGNoYWxrLnllbGxvdygnaGVsbG8gbXNnMicpLFxuICAgIGNoYWxrLmJvbGQoJ2hlbGxvIG1zZzMnKSxcbiAgXSkpLnRvRXF1YWwoW1xuICAgICcqKioqKioqKioqKioqKioqKionLFxuICAgICcqKiogaGVsbG8gbXNnMSAqKionLFxuICAgIGAqKiogJHtjaGFsay55ZWxsb3coJ2hlbGxvIG1zZzInKX0gKioqYCxcbiAgICBgKioqICR7Y2hhbGsuYm9sZCgnaGVsbG8gbXNnMycpfSAqKipgLFxuICAgICcqKioqKioqKioqKioqKioqKionLFxuICBdKSk7XG4iXX0=