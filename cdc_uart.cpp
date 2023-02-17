/*
 * The MIT License (MIT)
 *
 * Copyright (c) 2021 Raspberry Pi (Trading) Ltd.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 */

#include <pico/stdlib.h>

#include "tusb.h"


uint cdc_task(uint8_t *buf, size_t buf_len) {

    if (tud_cdc_connected()) {
        if (tud_cdc_available()) {
            return tud_cdc_read(buf, buf_len);
        }
    }

    return 0;
}

void tud_cdc_line_coding_cb(uint8_t itf, cdc_line_coding_t const* line_coding) {
    // This we don't need because it changes the HW serial baud rate
    // when the USB baud rate changes... for... some... reason?!?
    //picoprobe_info("New baud rate %d\n", line_coding->bit_rate);
    //uart_init(PICOPROBE_UART_INTERFACE, line_coding->bit_rate);
}
