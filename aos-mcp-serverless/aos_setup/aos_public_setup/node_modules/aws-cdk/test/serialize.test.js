"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
/* eslint-disable import/order */
const serialize_1 = require("../lib/serialize");
describe(serialize_1.toYAML, () => {
    test('does not wrap lines', () => {
        const longString = 'Long string is long!'.repeat(1024);
        expect((0, serialize_1.toYAML)({ longString })).toEqual(`longString: ${longString}\n`);
    });
});
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoic2VyaWFsaXplLnRlc3QuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyJzZXJpYWxpemUudGVzdC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOztBQUFBLGlDQUFpQztBQUNqQyxnREFBMEM7QUFFMUMsUUFBUSxDQUFDLGtCQUFNLEVBQUUsR0FBRyxFQUFFO0lBQ3BCLElBQUksQ0FBQyxxQkFBcUIsRUFBRSxHQUFHLEVBQUU7UUFDL0IsTUFBTSxVQUFVLEdBQUcsc0JBQXNCLENBQUMsTUFBTSxDQUFDLElBQUssQ0FBQyxDQUFDO1FBQ3hELE1BQU0sQ0FBQyxJQUFBLGtCQUFNLEVBQUMsRUFBRSxVQUFVLEVBQUUsQ0FBQyxDQUFDLENBQUMsT0FBTyxDQUFDLGVBQWUsVUFBVSxJQUFJLENBQUMsQ0FBQztJQUN4RSxDQUFDLENBQUMsQ0FBQztBQUNMLENBQUMsQ0FBQyxDQUFDIiwic291cmNlc0NvbnRlbnQiOlsiLyogZXNsaW50LWRpc2FibGUgaW1wb3J0L29yZGVyICovXG5pbXBvcnQgeyB0b1lBTUwgfSBmcm9tICcuLi9saWIvc2VyaWFsaXplJztcblxuZGVzY3JpYmUodG9ZQU1MLCAoKSA9PiB7XG4gIHRlc3QoJ2RvZXMgbm90IHdyYXAgbGluZXMnLCAoKSA9PiB7XG4gICAgY29uc3QgbG9uZ1N0cmluZyA9ICdMb25nIHN0cmluZyBpcyBsb25nIScucmVwZWF0KDFfMDI0KTtcbiAgICBleHBlY3QodG9ZQU1MKHsgbG9uZ1N0cmluZyB9KSkudG9FcXVhbChgbG9uZ1N0cmluZzogJHtsb25nU3RyaW5nfVxcbmApO1xuICB9KTtcbn0pO1xuIl19