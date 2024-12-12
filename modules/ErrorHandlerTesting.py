import unittest
import utilities.ErrorHandler as e


message = "Test message"
code = 70
t = unittest.TestCase()
custom_error = e.CustomError(message, code)
ui_error = e.IuError(message, code)
is_orienteering_error = e.IsOrieteeringApiError(message, code)
calendar_error = e.GoogleCalendarServicesError(message, code)
sandberg_error = e.SandbergDatabaseError(message, code)
handler_error = e.HandlerError(message, code)
names = ['CustomError', 'IuError', 'IsOrieteeringApiError', 'GoogleCalendarServicesError', 'SandbergDatabaseError', 'HandlerError']
errors = [custom_error, ui_error, is_orienteering_error, calendar_error, sandberg_error, handler_error]
for i, er in enumerate(errors):
    t.assertEqual(er.message, message)
    t.assertEqual(er.code, code)
    t.assertEqual(er.name, names[i])
    t.assertEqual(f'{names[i]}: {code} {message}', str(er))
    t.assertEqual(f'{names[i]}: {code} {message}', repr(er))
    print(f'Tests for {names[i]} run sucesfully')