"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
/* eslint-disable import/order */
const validate_notification_arn_1 = require("../../lib/util/validate-notification-arn");
describe('validate sns arns', () => {
    test('empty string', () => {
        const arn = '';
        expect((0, validate_notification_arn_1.validateSnsTopicArn)(arn)).toEqual(false);
    });
    test('colon in topic name', () => {
        const arn = 'arn:aws:sns:eu-west-1:abc:foo';
        expect((0, validate_notification_arn_1.validateSnsTopicArn)(arn)).toEqual(false);
    });
    test('missing :aws: in arn', () => {
        const arn = 'arn:sns:eu-west-1:foobar';
        expect((0, validate_notification_arn_1.validateSnsTopicArn)(arn)).toEqual(false);
    });
    test('dash in topic name', () => {
        const arn = 'arn:aws:sns:eu-west-1:123456789876:foo-bar';
        expect((0, validate_notification_arn_1.validateSnsTopicArn)(arn)).toEqual(true);
    });
    test('underscore in topic name', () => {
        const arn = 'arn:aws:sns:eu-west-1:123456789876:foo-bar_baz';
        expect((0, validate_notification_arn_1.validateSnsTopicArn)(arn)).toEqual(true);
    });
});
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidmFsaWRhdGUtbm90aWZpY2F0aW9uLWFybi50ZXN0LmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsidmFsaWRhdGUtbm90aWZpY2F0aW9uLWFybi50ZXN0LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7O0FBQUEsaUNBQWlDO0FBQ2pDLHdGQUErRTtBQUUvRSxRQUFRLENBQUMsbUJBQW1CLEVBQUUsR0FBRyxFQUFFO0lBQ2pDLElBQUksQ0FBQyxjQUFjLEVBQUUsR0FBRyxFQUFFO1FBQ3hCLE1BQU0sR0FBRyxHQUFHLEVBQUUsQ0FBQztRQUNmLE1BQU0sQ0FBQyxJQUFBLCtDQUFtQixFQUFDLEdBQUcsQ0FBQyxDQUFDLENBQUMsT0FBTyxDQUFDLEtBQUssQ0FBQyxDQUFDO0lBQ2xELENBQUMsQ0FBQyxDQUFDO0lBRUgsSUFBSSxDQUFDLHFCQUFxQixFQUFFLEdBQUcsRUFBRTtRQUMvQixNQUFNLEdBQUcsR0FBRywrQkFBK0IsQ0FBQztRQUM1QyxNQUFNLENBQUMsSUFBQSwrQ0FBbUIsRUFBQyxHQUFHLENBQUMsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxLQUFLLENBQUMsQ0FBQztJQUNsRCxDQUFDLENBQUMsQ0FBQztJQUVILElBQUksQ0FBQyxzQkFBc0IsRUFBRSxHQUFHLEVBQUU7UUFDaEMsTUFBTSxHQUFHLEdBQUcsMEJBQTBCLENBQUM7UUFDdkMsTUFBTSxDQUFDLElBQUEsK0NBQW1CLEVBQUMsR0FBRyxDQUFDLENBQUMsQ0FBQyxPQUFPLENBQUMsS0FBSyxDQUFDLENBQUM7SUFDbEQsQ0FBQyxDQUFDLENBQUM7SUFFSCxJQUFJLENBQUMsb0JBQW9CLEVBQUUsR0FBRyxFQUFFO1FBQzlCLE1BQU0sR0FBRyxHQUFHLDRDQUE0QyxDQUFDO1FBQ3pELE1BQU0sQ0FBQyxJQUFBLCtDQUFtQixFQUFDLEdBQUcsQ0FBQyxDQUFDLENBQUMsT0FBTyxDQUFDLElBQUksQ0FBQyxDQUFDO0lBQ2pELENBQUMsQ0FBQyxDQUFDO0lBRUgsSUFBSSxDQUFDLDBCQUEwQixFQUFFLEdBQUcsRUFBRTtRQUNwQyxNQUFNLEdBQUcsR0FBRyxnREFBZ0QsQ0FBQztRQUM3RCxNQUFNLENBQUMsSUFBQSwrQ0FBbUIsRUFBQyxHQUFHLENBQUMsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUMsQ0FBQztJQUNqRCxDQUFDLENBQUMsQ0FBQztBQUNMLENBQUMsQ0FBQyxDQUFDIiwic291cmNlc0NvbnRlbnQiOlsiLyogZXNsaW50LWRpc2FibGUgaW1wb3J0L29yZGVyICovXG5pbXBvcnQgeyB2YWxpZGF0ZVNuc1RvcGljQXJuIH0gZnJvbSAnLi4vLi4vbGliL3V0aWwvdmFsaWRhdGUtbm90aWZpY2F0aW9uLWFybic7XG5cbmRlc2NyaWJlKCd2YWxpZGF0ZSBzbnMgYXJucycsICgpID0+IHtcbiAgdGVzdCgnZW1wdHkgc3RyaW5nJywgKCkgPT4ge1xuICAgIGNvbnN0IGFybiA9ICcnO1xuICAgIGV4cGVjdCh2YWxpZGF0ZVNuc1RvcGljQXJuKGFybikpLnRvRXF1YWwoZmFsc2UpO1xuICB9KTtcblxuICB0ZXN0KCdjb2xvbiBpbiB0b3BpYyBuYW1lJywgKCkgPT4ge1xuICAgIGNvbnN0IGFybiA9ICdhcm46YXdzOnNuczpldS13ZXN0LTE6YWJjOmZvbyc7XG4gICAgZXhwZWN0KHZhbGlkYXRlU25zVG9waWNBcm4oYXJuKSkudG9FcXVhbChmYWxzZSk7XG4gIH0pO1xuXG4gIHRlc3QoJ21pc3NpbmcgOmF3czogaW4gYXJuJywgKCkgPT4ge1xuICAgIGNvbnN0IGFybiA9ICdhcm46c25zOmV1LXdlc3QtMTpmb29iYXInO1xuICAgIGV4cGVjdCh2YWxpZGF0ZVNuc1RvcGljQXJuKGFybikpLnRvRXF1YWwoZmFsc2UpO1xuICB9KTtcblxuICB0ZXN0KCdkYXNoIGluIHRvcGljIG5hbWUnLCAoKSA9PiB7XG4gICAgY29uc3QgYXJuID0gJ2Fybjphd3M6c25zOmV1LXdlc3QtMToxMjM0NTY3ODk4NzY6Zm9vLWJhcic7XG4gICAgZXhwZWN0KHZhbGlkYXRlU25zVG9waWNBcm4oYXJuKSkudG9FcXVhbCh0cnVlKTtcbiAgfSk7XG5cbiAgdGVzdCgndW5kZXJzY29yZSBpbiB0b3BpYyBuYW1lJywgKCkgPT4ge1xuICAgIGNvbnN0IGFybiA9ICdhcm46YXdzOnNuczpldS13ZXN0LTE6MTIzNDU2Nzg5ODc2OmZvby1iYXJfYmF6JztcbiAgICBleHBlY3QodmFsaWRhdGVTbnNUb3BpY0Fybihhcm4pKS50b0VxdWFsKHRydWUpO1xuICB9KTtcbn0pO1xuXG4iXX0=