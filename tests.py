from math import floor
import numpy as np
import unittest

from convolution import convolve, add_padding


class TestConvolution(unittest.TestCase):
    def test_paddings_shape(self, N: int = 1000):
        for _ in range(N):
            m_h = np.random.randint(3, 100)
            m_w = np.random.randint(3, 100)
            random_data = np.random.rand(m_h, m_w)

            rows, cols = np.random.randint(0, 100, 2)
            random_data_with_padding = add_padding(random_data, (rows, cols))
            
            self.assertEqual(random_data_with_padding.shape, (m_h + rows*2, m_w + cols*2))


    def test_random_case(self, N: int = 1000):
        for _ in range(N): 
            d = np.random.randint(1, 100, 2)
            k = np.random.choice([1, 3, 5, 7, 9, 10], 2) # `10` is to check oddness assertion
            random_data = np.random.rand(*d)
            random_kernel = np.random.rand(*k)
            for __ in range(N):
                stride = np.random.randint(0, 5, 2) # `0` is to check parameters assertion
                dilation = np.random.randint(0, 5, 2) # `0` is to check parameters assertion
                padding = np.random.randint(-1, 5, 2) # `-1` is to check parameters assertion
                try: # `try` in case of division by zero when stride[0] or stride[1] equal to zero
                    h_out = floor((d[0] + 2 * padding[0] - k[0] - (k[0] - 1) * (dilation[0] - 1)) / stride[0]) + 1
                    w_out = floor((d[1] + 2 * padding[1] - k[1] - (k[1] - 1) * (dilation[1] - 1)) / stride[1]) + 1
                except:
                    h_out, w_out = None, None
                # print(f'Data: {d} | Kern: {k} | Stri: {stride} | Dila: {dilation} | Padd: {padding} | OutD: {h_out, w_out}') # for debugging
                
                if (stride[0] < 1 or stride[1] < 1 or dilation[0] < 1 or dilation[1] < 1 or padding[0] < 0 or padding[1] < 0 or
                    not isinstance(stride[0], int) or not isinstance(stride[1], int) or not isinstance(dilation[0], int) or 
                    not isinstance(dilation[1], int) or not isinstance(padding[0], int) or not isinstance(padding[1], int)):
                    with self.assertRaises(AssertionError):
                        data_conved = convolve(random_data, random_kernel, stride=stride, dilation=dilation, padding=padding)
                elif k[0] % 2 != 1 or k[1] % 2 != 1:
                    with self.assertRaises(AssertionError):
                        data_conved = convolve(random_data, random_kernel, stride=stride, dilation=dilation, padding=padding)
                elif d[0] < k[0] or d[1] < k[1]:
                    with self.assertRaises(AssertionError):
                        data_conved = convolve(random_data, random_kernel, stride=stride, dilation=dilation, padding=padding)
                elif h_out <= 0 or w_out <= 0:
                    with self.assertRaises(AssertionError):
                        data_conved = convolve(random_data, random_kernel, stride=stride, dilation=dilation, padding=padding)
                else:
                    data_conved = convolve(random_data, random_kernel, stride=stride, dilation=dilation, padding=padding)
                    self.assertEqual(data_conved.shape, (h_out, w_out))


    def test_kernel_3x3(self):
        data = np.array([[0, 4, 3, 2, 0, 1, 0], 
                         [4, 3, 0, 1, 0, 1, 0],
                         [1, 3, 4, 2, 0, 1, 0],
                         [3, 4, 2, 2, 0, 1, 0],
                         [0, 0, 0, 0, 0, 1, 0]])

        kernel = np.array([[1, 1, 3], 
                           [0, 2, 3],
                           [3, 3, 3]])

        # stride = 1, dilation = 1, padding = 0
        result_110 = convolve(data, kernel)
        answer_110 = np.array([[43, 43, 25, 17, 6], 
                               [52, 44, 17, 16, 6],
                               [30, 23, 10, 11, 6]])
        
        # stride = 1, dilation = 1, padding = 1
        result_111 = convolve(data, kernel, padding=(1, 1))
        answer_111 = np.array([[33, 38, 24,  7,  9,  5,  3],
                               [41, 43, 43, 25, 17,  6,  4],
                               [45, 52, 44, 17, 16,  6,  4],
                               [28, 30, 23, 10, 11,  6,  4],
                               [15, 13, 12,  4,  8,  3,  1]])
        
        # stride = 1, dilation = 2, padding = 0
        result_120 = convolve(data, kernel, dilation=(2, 2))
        answer_120 = np.array([[11, 19, 3]])

        # stride = 1, dilation = 2, padding = 1
        result_121 = convolve(data, kernel, dilation=(2, 2), padding=(1, 1))
        answer_121 = np.array([[27, 15, 26,  6, 11],
                               [22, 11, 19,  3,  8],
                               [20,  8, 14,  0,  4]])
        
        # stride = 2, dilation = 1, padding = 0
        result_210 = convolve(data, kernel, stride=(2, 2))
        answer_210 = np.array([[43, 25, 6], 
                               [30, 10, 6]])
        
        # stride = 2, dilation = 1, padding = 1
        result_211 = convolve(data, kernel, stride=(2, 2), padding=(1, 1))
        answer_211 = np.array([[33, 24,  9,  3],
                               [45, 44, 16,  4],
                               [15, 12,  8,  1]])
        
        # stride = 2, dilation = 2, padding = 0
        result_220 = convolve(data, kernel, stride=(2, 2), dilation=(2, 2))
        answer_220 = np.array([[11, 3]])

        # stride = 2, dilation = 2, padding = 1
        result_221 = convolve(data, kernel, stride=(2, 2), dilation=(2, 2), padding=(1, 1))
        answer_221 = np.array([[27, 26, 11], 
                               [20, 14,  4]])

        self.assertEqual(result_110.tolist(), answer_110.tolist())
        self.assertEqual(result_111.tolist(), answer_111.tolist())
        self.assertEqual(result_120.tolist(), answer_120.tolist())
        self.assertEqual(result_121.tolist(), answer_121.tolist())
        self.assertEqual(result_210.tolist(), answer_210.tolist())
        self.assertEqual(result_211.tolist(), answer_211.tolist())
        self.assertEqual(result_220.tolist(), answer_220.tolist())
        self.assertEqual(result_221.tolist(), answer_221.tolist())


    def test_kernel_7x7(self):
        pass


if __name__ == '__main__':
    unittest.main()
