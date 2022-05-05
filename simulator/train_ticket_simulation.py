import datetime
import json
import os
import random
import subprocess as sp
import sys
import time
import numpy as np
from scipy.interpolate import interp1d
import threading
from data_processing_simulator import process_utlization, get_current_configs
from navigation_slo_threshold_simulator import get_stopping_threshold, save_q_value
from db_simulator import HistoryDB, QValueDB

container_list = ['ts-assurance-service', 'ts-auth-service', 'ts-basic-service', 'ts-config-service',
                  'ts-consign-price-service', 'ts-consign-service', 'ts-contacts-service', 'ts-food-map-service',
                  'ts-food-service', 'ts-order-other-service', 'ts-order-service', 'ts-preserve-other-service',
                  'ts-preserve-service', 'ts-price-service', 'ts-route-plan-service', 'ts-route-service',
                  'ts-seat-service', 'ts-security-service', 'ts-station-service', 'ts-ticketinfo-service',
                  'ts-train-service', 'ts-travel-plan-service', 'ts-travel-service', 'ts-travel2-service',
                  'ts-ui-dashboard', 'ts-user-service', 'ts-rebook-service', 'ts-ticket-office-service']
EXPERIMENT_TIME = 120  # seconds
THROTTLE_PERCENTAGE = 0.01  # 1%
container_util_list = {'ts-assurance-service': [],
                       'ts-basic-service': [],
                       'ts-config-service': [],
                       'ts-consign-price-service': [],
                       'ts-consign-service': [],
                       'ts-contacts-service': [],
                       'ts-food-map-service': [],
                       'ts-food-service': [],
                       'ts-auth-service': [],
                       'ts-order-other-service': [],
                       'ts-order-service': [],
                       'ts-preserve-other-service': [],
                       'ts-preserve-service': [],
                       'ts-price-service': [],
                       'ts-route-plan-service': [],
                       'ts-route-service': [],
                       'ts-seat-service': [],
                       'ts-security-service': [],
                       'ts-user-service': [],
                       'ts-station-service': [],
                       'ts-ticketinfo-service': [],
                       'ts-train-service': [],
                       'ts-travel2-service': [],
                       'ts-travel-plan-service': [],
                       'ts-travel-service': []}
DEFAULT_CONFIGS = {'ts-assurance-service': 2.0, 'ts-basic-service': 4, 'ts-config-service': 2.5,
                   'ts-consign-price-service': 2, 'ts-consign-service': 2, 'ts-contacts-service': 2.5,
                   'ts-food-map-service': 2, 'ts-food-service': 2.5, 'ts-auth-service': 10.5,
                   'ts-order-other-service': 2.5, 'ts-order-service': 5,
                   'ts-preserve-other-service': 2, 'ts-preserve-service': 4, 'ts-price-service': 2.5,
                   'ts-route-plan-service': 2, 'ts-route-service': 4, 'ts-seat-service': 5, 'ts-security-service': 5,
                   'ts-user-service': 2,
                   'ts-station-service': 5, 'ts-ticketinfo-service': 3, 'ts-train-service': 2,
                   'ts-travel2-service': 5, 'ts-travel-plan-service': 2, 'ts-travel-service': 5}
default = 10
container_limits = {'ts-assurance-service': default, 'ts-basic-service': default, 'ts-config-service': default,
                    'ts-consign-price-service': default, 'ts-consign-service': default, 'ts-contacts-service': default,
                    'ts-food-map-service': default, 'ts-food-service': default, 'ts-auth-service': default,
                    'ts-order-other-service': default, 'ts-order-service': default,
                    'ts-preserve-other-service': default, 'ts-preserve-service': default, 'ts-price-service': default,
                    'ts-route-plan-service': default, 'ts-route-service': default, 'ts-seat-service': default,
                    'ts-security-service': default,
                    'ts-user-service': default,
                    'ts-station-service': default, 'ts-ticketinfo-service': default, 'ts-train-service': default,
                    'ts-travel2-service': default, 'ts-travel-plan-service': default, 'ts-travel-service': default}

request_per_seconds = [217, 216, 216, 216, 215, 215, 214, 211, 209, 203, 197, 188, 179, 167, 157, 144, 135, 124, 116,
                       108, 104, 100, 98, 97, 97, 98, 99, 102, 103, 107, 109, 114, 117, 124, 130, 139, 146, 156, 163,
                       172, 177, 187, 193, 206, 217, 231, 243, 258, 268, 279, 283, 288, 290, 293, 294, 295, 296, 298,
                       300, 303, 306, 309, 312, 315, 318, 321, 324, 326, 328, 329, 330, 331, 332, 333, 333, 332, 330,
                       327, 323, 316, 309, 300, 293, 285, 280, 275, 273, 271, 272, 273, 274, 276, 277, 278, 278, 278,
                       277, 274, 271, 265, 259, 250, 243, 233, 224, 212, 202, 190, 180, 167, 157, 145, 136, 125, 118,
                       110, 105, 101, 99, 98, 98, 98, 100, 101, 103, 105, 107, 111, 114, 120, 126, 135, 143, 154, 164,
                       178, 189, 203, 213, 226, 235, 246, 254, 263, 269, 275, 280, 284, 287, 290, 291, 293, 295, 296,
                       298, 299, 301, 302, 303, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 315, 314, 314,
                       311, 308, 302, 297, 289, 283, 276, 271, 266, 263, 261, 261, 260, 260, 260, 261, 261, 261, 261,
                       261, 260, 258, 255, 251, 245, 239, 229, 221, 210, 200, 187, 177, 164, 154, 142, 133, 122, 115,
                       106, 101, 96, 94, 92, 92, 92, 93, 95, 97, 99, 101, 105, 109, 114, 119, 128, 135, 147, 156, 169,
                       181, 195, 207, 221, 231, 244, 252, 262, 268, 276, 281, 286, 288, 291, 292, 294, 293, 293, 293,
                       294, 295, 296, 298, 301, 303, 305, 307, 310, 312, 314, 315, 316, 317, 318, 319, 319, 319, 316,
                       313, 308, 302, 294, 287, 277, 269, 262, 257, 253, 252, 251, 253, 256, 259, 262, 264, 265, 264,
                       263, 261, 257, 253, 246, 241, 232, 225, 214, 205, 192, 182, 169, 159, 147, 137, 126, 118, 109,
                       103, 99, 97, 96, 95, 95, 96, 98, 99, 100, 101, 104, 107, 112, 116, 124, 131, 142, 151, 163, 174,
                       189, 201, 215, 225, 238, 246, 256, 262, 269, 274, 279, 281, 284, 286, 287, 287, 288, 288, 289,
                       291, 292, 294, 296, 298, 300, 302, 304, 306, 308, 309, 310, 311, 312, 312, 313, 313, 310, 308,
                       303, 297, 290, 282, 272, 264, 257, 252, 248, 246, 244, 245, 246, 246, 247, 248, 248, 248, 247,
                       246, 243, 240, 235, 230, 222, 215, 205, 197, 185, 175, 163, 153, 140, 131, 120, 113, 104, 98, 92,
                       88, 85, 83, 82, 82, 83, 83, 85, 86, 88, 91, 95, 98, 105, 111, 121, 129, 141, 152, 166, 177, 191,
                       201, 214, 223, 233, 239, 246, 250, 255, 259, 262, 264, 265, 266, 265, 264, 263, 262, 261, 261,
                       261, 261, 262, 262, 262, 263, 263, 263, 263, 263, 262, 262, 261, 260, 257, 254, 250, 245, 238,
                       232, 223, 215, 206, 198, 189, 183, 176, 172, 168, 165, 162, 161, 160, 160, 161, 161, 162, 162,
                       161, 160, 158, 156, 152, 148, 142, 137, 131, 125, 118, 112, 105, 99, 91, 86, 79, 74, 68, 65, 61,
                       58, 57, 56, 55, 56, 57, 58, 60, 61, 64, 67, 71, 76, 82, 87, 94, 100, 108, 115, 124, 131, 140,
                       147, 155, 162, 170, 176, 183, 187, 192, 196, 200, 202, 205, 206, 208, 210, 211, 212, 213, 214,
                       215, 216, 217, 218, 220, 222, 224, 225, 226, 227, 227, 226, 224, 221, 217, 213, 208, 204, 199,
                       194, 189, 185, 180, 177, 173, 171, 170, 169, 169, 169, 170, 171, 171, 172, 172, 171, 169, 167,
                       164, 161, 156, 152, 146, 142, 135, 130, 122, 116, 109, 103, 96, 90, 84, 80, 75, 72, 69, 68, 67,
                       68, 69, 70, 72, 74, 77, 79, 83, 87, 93, 98, 105, 112, 120, 127, 137, 144, 153, 160, 169, 176,
                       184, 191, 198, 204, 211, 216, 223, 227, 233, 238, 243, 248, 253, 258, 262, 265, 269, 271, 273,
                       274, 274, 274, 274, 274, 274, 274, 273, 273, 273, 271, 269, 266, 262, 259, 254, 251, 248, 247,
                       246, 247, 247, 248, 249, 249, 249, 248, 248, 248, 247, 247, 246, 245, 241, 238, 231, 224, 214,
                       205, 192, 183, 170, 160, 148, 139, 128, 120, 112, 106, 100, 97, 94, 93, 93, 94, 95, 97, 98, 100,
                       103, 106, 110, 114, 121, 128, 138, 146, 159, 169, 184, 195, 209, 220, 233, 242, 253, 260, 268,
                       274, 280, 284, 289, 292, 295, 297, 300, 303, 306, 308, 312, 314, 318, 320, 323, 325, 328, 330,
                       332, 334, 336, 337, 338, 340, 340, 339, 336, 333, 327, 320, 312, 304, 294, 287, 280, 275, 272,
                       270, 269, 269, 270, 270, 269, 268, 267, 266, 264, 262, 259, 256, 251, 246, 237, 230, 220, 210,
                       197, 187, 173, 163, 149, 140, 128, 121, 112, 106, 99, 96, 93, 91, 90, 91, 92, 94, 96, 98, 102,
                       105, 110, 114, 121, 129, 139, 148, 162, 173, 189, 201, 215, 226, 239, 248, 258, 265, 272, 277,
                       283, 286, 291, 294, 297, 300, 303, 305, 308, 310, 312, 313, 315, 317, 319, 320, 322, 324, 326,
                       327, 328, 328, 328, 328, 327, 326, 324, 322, 317, 313, 306, 299, 289, 281, 273, 268, 263, 261,
                       259, 260, 261, 261, 262, 262, 262, 263, 262, 260, 258, 256, 251, 246, 238, 232, 222, 214, 201,
                       191, 178, 168, 154, 144, 132, 124, 115, 109, 102, 98, 95, 93, 92, 92, 92, 92, 94, 95, 98, 102,
                       107, 111, 120, 126, 137, 146, 159, 170, 185, 197, 212, 223, 236, 245, 256, 263, 272, 279, 286,
                       290, 295, 298, 301, 302, 303, 304, 305, 307, 309, 311, 313, 315, 317, 319, 321, 322, 323, 324,
                       324, 325, 325, 325, 325, 326, 324, 322, 318, 314, 308, 301, 292, 284, 274, 266, 260, 257, 254,
                       254, 253, 256, 258, 258, 258, 259, 258, 257, 254, 252, 248, 244, 237, 231, 222, 215, 204, 195,
                       182, 172, 160, 150, 138, 129, 119, 113, 105, 101, 95, 92, 89, 88, 87, 87, 89, 91, 95, 98, 104,
                       108, 116, 122, 133, 141, 154, 164, 179, 192, 207, 219, 233, 243, 255, 262, 271, 277, 284, 288,
                       293, 296, 298, 299, 301, 301, 302, 303, 305, 306, 308, 310, 312, 313, 315, 316, 318, 319, 320,
                       320, 320, 320, 319, 318, 316, 315, 311, 307, 301, 295, 286, 279, 270, 264, 256, 252, 247, 245,
                       242, 242, 241, 241, 240, 239, 238, 236, 234, 233, 230, 228, 223, 218, 211, 205, 195, 186, 174,
                       164, 151, 142, 130, 122, 112, 106, 96, 89, 84, 82, 80, 79, 78, 80, 84, 84, 86, 87, 91, 94, 99,
                       104, 113, 120, 131, 140, 153, 164, 179, 190, 203, 213, 224, 232, 240, 245, 251, 256, 260, 263,
                       265, 266, 267, 267, 266, 265, 264, 264, 263, 263, 263, 264, 264, 264, 263, 263, 263, 262, 261,
                       261, 260, 260, 260, 259, 257, 255, 252, 248, 242, 237, 229, 223, 215, 208, 199, 193, 185, 180,
                       175, 171, 168, 167, 165, 164, 163, 163, 162, 161, 159, 158, 156, 154, 150, 147, 141, 137, 130,
                       125, 117, 111, 104, 98, 91, 86, 80, 76, 71, 67, 64, 62, 61, 60, 60, 61, 63, 64, 67, 69, 73, 77,
                       82, 87, 94, 101, 109, 116, 125, 132, 142, 149, 158, 165, 173, 179, 186, 190, 195, 199, 203, 206,
                       209, 211, 213, 215, 217, 218, 220, 221, 223, 224, 225, 226, 226, 227, 227, 227, 227, 227, 227,
                       227, 226, 225, 223, 221, 218, 216, 211, 207, 203, 199, 194, 190, 187, 185, 183, 183, 182, 183,
                       183, 184, 184, 185, 185, 185, 184, 183, 180, 177, 172, 168, 162, 157, 150, 145, 138, 133, 125,
                       120, 112, 107, 100, 95, 89, 85, 82, 80, 78, 78, 78, 79, 81, 82, 84, 85, 88, 91, 95, 98, 104, 109,
                       116, 123, 132, 139, 149, 156, 166, 174, 183, 189, 198, 204, 211, 217, 223, 228, 234, 238, 243,
                       247, 252, 256, 260, 264, 269, 272, 276, 279, 282, 285, 288, 290, 292, 294, 295, 295, 295, 294,
                       292, 291, 289, 287, 282, 279, 276, 274, 272, 271, 267, 264, 258, 253, 247, 241, 233, 225, 224,
                       223, 221, 216, 205, 201, 193, 178, 168, 155, 146, 138, 127, 123, 117, 112, 105, 99, 98, 95, 92,
                       95, 96, 100, 106, 111, 114, 121, 128, 134, 145, 150, 153, 163, 172, 177, 185, 185, 198, 214, 232,
                       245, 260, 276, 289, 296, 297, 297, 297, 295, 292, 297, 304, 312, 314, 317, 318, 317, 319, 322,
                       324, 330, 329, 337, 340, 333, 332, 331, 321, 331, 326, 328, 327, 321, 313, 311, 296, 288, 277,
                       277, 268, 272, 275, 275, 275, 276, 272, 273, 268, 268, 271, 269, 272, 277, 270, 269, 254, 245,
                       236, 224, 205, 196, 181, 171, 157, 148, 135, 127, 120, 109, 106, 105, 99, 97, 93, 93, 97, 98, 96,
                       102, 106, 109, 110, 111, 118, 122, 127, 136, 153, 161, 179, 183, 198, 208, 223, 231, 246, 253,
                       262, 274, 283, 278, 278, 278, 273, 281, 274, 274, 281, 284, 289, 293, 298, 298, 300, 300, 302,
                       297, 303, 300, 309, 313, 312, 311, 316, 317, 311, 306, 295, 290, 290, 290, 284, 286, 281, 277,
                       273, 271, 268, 265, 262, 257, 265, 274, 271, 266, 264, 264, 270, 269, 257, 256, 249, 239, 225,
                       214, 198, 191, 178, 172, 164, 157, 143, 133, 125, 115, 107, 101, 95, 95, 92, 86, 90, 92, 96, 101,
                       104, 110, 118, 117, 120, 125, 128, 135, 144, 148, 163, 178, 192, 209, 227, 236, 255, 268, 274,
                       279, 286, 286, 289, 287, 284, 281, 285, 278, 277, 282, 287, 288, 290, 286, 289, 294, 295, 297,
                       300, 305, 308, 309, 307, 308, 307, 311, 315, 321, 323, 326, 321, 313, 303, 294, 281, 272, 260,
                       251, 248, 240, 244, 247, 255, 257, 263, 267, 274, 269, 267, 258, 257, 256, 247, 239, 229, 217,
                       209, 200, 184, 172, 161, 150, 140, 129, 117, 110, 104, 100, 98, 98, 98, 94, 96, 95, 98, 97, 99,
                       100, 104, 107, 116, 116, 129, 136, 144, 156, 170, 179, 194, 201, 209, 223, 234, 242, 250, 261,
                       269, 282, 283, 283, 288, 292, 289, 292, 291, 299, 299, 299, 302, 305, 306, 309, 311, 310, 311,
                       303, 303, 309, 301, 305, 306, 306, 308, 304, 296, 296, 282, 280, 271, 266, 261, 254, 249, 247,
                       242, 240, 237, 233, 229, 233, 235, 239, 244, 245, 244, 244, 238, 237, 234, 226, 217, 214, 207,
                       199, 184, 168, 154, 150, 139, 133, 124, 115, 110, 104, 96, 89, 84, 79, 79, 78, 77, 77, 82, 82,
                       86, 87, 92, 97, 103, 110, 120, 127, 140, 152, 164, 176, 188, 203, 220, 227, 239, 249, 251, 252,
                       253, 251, 261, 263, 264, 273, 279, 279, 282, 282, 273, 274, 270, 267, 271, 263, 256, 265, 261,
                       260, 265, 260, 266, 272, 264, 264, 261, 255, 252, 247, 235, 235, 229, 224, 217, 210, 198, 195,
                       182, 177, 173, 164, 160, 164, 161, 164, 158, 156, 160, 163, 157, 159, 154, 156, 154, 153, 148,
                       145, 138, 133, 127, 120, 107, 99, 94, 89, 85, 79, 72, 68, 63, 57, 52, 50, 50, 53, 55, 56, 62, 63,
                       68, 68, 73, 78, 86, 91, 101, 103, 111, 114, 120, 126, 136, 140, 149, 159, 171, 181, 183, 184,
                       192, 199, 206, 203, 208, 211, 211, 207, 211, 206, 208, 204, 205, 206, 211, 214, 216, 223, 224,
                       231, 237, 241, 237, 234, 227, 229, 217, 207, 197, 196, 194, 193, 185, 188, 187, 189, 179, 174,
                       171, 171, 164, 163, 159, 162, 163, 159, 161, 165, 162, 164, 159, 156, 153, 150, 142, 142, 132,
                       127, 122, 115, 107, 106, 97, 92, 87, 80, 77, 70, 64, 63, 60, 61, 64, 65, 70, 75, 78, 81, 87, 92,
                       100, 107, 111, 118, 131, 139, 146, 149, 157, 164, 175, 178, 189, 197, 208, 217, 230, 234, 238,
                       242, 246, 246, 248, 252, 255, 260, 260, 260, 264, 263, 265, 264, 262, 261, 268, 267, 273, 270,
                       267, 273, 272, 269, 271, 265, 258, 254, 247, 247, 246, 244, 241, 241, 243, 248, 243, 240, 243,
                       249, 252, 257, 257, 263, 264, 257, 249, 246, 239, 226, 212, 205, 197, 187, 174, 164, 154, 148,
                       131, 122, 112, 107, 98, 98, 97, 98, 98, 99, 98, 100, 99, 95, 99, 99, 104, 109, 115, 125, 140,
                       151, 165, 177, 190, 203, 211, 222, 228, 237, 245, 253, 268, 282, 279, 291, 296, 298, 305, 306,
                       310, 315, 319, 319, 323, 326, 323, 319, 320, 320, 328, 329, 325, 331, 340, 349, 343, 341, 345,
                       347, 337, 325, 322, 324, 320, 309, 296, 295, 289, 279, 276, 273, 272, 278, 275, 274, 272, 262,
                       261, 263, 256, 256, 258, 256, 253, 246, 238, 235, 226, 216, 204, 195, 176, 164, 147, 134, 119,
                       111, 101, 98, 89, 87, 84, 85, 85, 86, 86, 89, 90, 94, 94, 95, 104, 110, 118, 127, 139, 148, 161,
                       175, 191, 205, 221, 228, 246, 253, 261, 268, 273, 273, 286, 287, 294, 297, 302, 304, 306, 306,
                       314, 314, 317, 321, 323, 330, 329, 321, 320, 315, 312, 319, 320, 325, 325, 327, 336, 330, 319,
                       318, 312, 314, 309, 302, 300, 298, 290, 285, 283, 286, 284, 280, 274, 275, 269, 260, 258, 254,
                       254, 258, 256, 258, 257, 250, 239, 232, 219, 206, 195, 187, 175, 167, 154, 147, 140, 128, 115,
                       110, 106, 102, 100, 96, 93, 93, 89, 88, 89, 89, 89, 94, 100, 109, 115, 124, 135, 146, 156, 165,
                       175, 192, 208, 215, 234, 245, 264, 273, 274, 273, 286, 285, 288, 292, 296, 300, 308, 303, 302,
                       304, 302, 307, 315, 311, 310, 311, 319, 322, 314, 317, 317, 324, 327, 322, 314, 317, 307, 307,
                       308, 301, 299, 296, 290, 290, 279, 268, 266, 255, 253, 251, 250, 258, 256, 259, 264, 268, 272,
                       265, 261, 264, 262, 259, 249, 240, 236, 226, 211, 197, 183, 170, 156, 143, 134, 126, 117, 108,
                       102, 97, 89, 86, 84, 86, 86, 86, 87, 89, 90, 92, 96, 101, 112, 121, 131, 142, 152, 160, 173, 186,
                       197, 214, 224, 235, 243, 248, 251, 258, 267, 272, 275, 286, 295, 300, 303, 301, 302, 305, 301,
                       298, 301, 307, 301, 303, 304, 312, 320, 318, 318, 327, 329, 338, 335, 332, 327, 327, 318, 313,
                       299, 293, 287, 288, 278, 270, 265, 262, 253, 248, 241, 234, 235, 230, 226, 225, 223, 220, 217,
                       213, 216, 219, 213, 209, 203, 197, 193, 179, 162, 154, 136, 127, 116, 104, 96, 93, 85, 83, 80,
                       78, 80, 81, 78, 81, 81, 81, 84, 86, 90, 92, 95, 99, 109, 119, 127, 134, 147, 163, 181, 194, 209,
                       215, 230, 241, 245, 243, 250, 254, 266, 269, 270, 271, 275, 269, 259, 253, 246, 244, 245, 247,
                       246, 248, 250, 251, 257, 256, 258, 265, 271, 269, 271, 264, 266, 259, 249, 240, 234, 232, 231,
                       227, 224, 224, 218, 219, 206, 196, 189, 184, 176, 175, 169, 164, 166, 161, 159, 159, 156, 153,
                       158, 153, 151, 147, 145, 142, 143, 135, 132, 125, 119, 111, 103, 96, 88, 84, 82, 78, 71, 68, 62,
                       60, 58, 55, 54, 57, 60, 60, 63, 64, 72, 77, 84, 86, 93, 102, 107, 108, 118, 123, 134, 146, 154,
                       163, 173, 176, 182, 191, 197, 202, 205, 209, 212, 213, 214, 215, 217, 224, 222, 225, 229, 232,
                       226, 225, 224, 225, 224, 224, 218, 219, 222, 220, 222, 221, 220, 216, 216, 208, 205, 202, 199,
                       196, 197, 194, 193, 187, 182, 178, 177, 177, 177, 181, 184, 188, 192, 189, 187, 184, 176, 171,
                       164, 162, 158, 152, 145, 142, 139, 133, 120, 114, 107, 104, 95, 90, 88, 87, 82, 81, 79, 81, 82,
                       82, 86, 87, 91, 88, 90, 91, 96, 96, 105, 111, 122, 130, 138, 143, 157, 165, 175, 178, 182, 189,
                       201, 202, 210, 215, 227, 239, 248, 245, 248, 246, 252, 249, 248, 248, 255, 259, 266, 262, 266,
                       274, 276, 276, 286, 293, 304, 308, 303, 301, 304, 300, 289, 287, 280, 276, 273, 265, 265, 271,
                       258, 249, 243, 240, 234, 226, 211, 212, 212, 213, 207, 209, 202, 201, 193, 185, 170, 163, 147,
                       135, 122, 114, 109, 105, 100, 100, 98, 102, 101, 101, 103, 105, 108, 113, 114, 115, 119, 126,
                       135, 143, 151, 163, 176, 183, 198, 203, 214, 226, 240, 249, 265, 268, 280, 283, 281, 281, 290,
                       290, 292, 291, 288, 289, 285, 284, 289, 293, 302, 312, 325, 333, 335, 339, 344, 345, 350, 341,
                       343, 343, 340, 334, 329, 314, 308, 305, 299, 290, 282, 271, 267, 273, 270, 267, 273, 282, 287,
                       289, 282, 283, 281, 277, 267, 267, 261, 260, 244, 243, 231, 224, 209, 207, 192, 183, 167, 155,
                       143, 136, 123, 113, 110, 106, 100, 101, 100, 99, 103, 102, 101, 102, 106, 109, 113, 116, 126,
                       131, 140, 149, 159, 167, 175, 180, 192, 208, 220, 224, 237, 251, 261, 271, 271, 270, 275, 280,
                       279, 280, 280, 282, 285, 291, 293, 297, 303, 302, 304, 303, 306, 302, 308, 304, 308, 309, 314,
                       311, 309, 304, 305, 307, 309, 301, 294, 292, 283, 281, 272, 264, 267, 265, 267, 267, 270, 270,
                       266, 265, 269, 269, 273]


def choose_containers(container_numbers, utilizations, throttles, current_configs):
    candidate_containers = {}
    for x in utilizations:
        # if throttles[x] > THROTTLE_PERCENTAGE * EXPERIMENT_TIME:  # 1 seconds
        #     continue
        if current_configs[x] <= 0.3:
            continue
        candidate_containers[x] = utilizations[x]

    artificial_utils = {}
    for x in candidate_containers.keys():
        artificial_utils[x] = candidate_containers[x] / container_limits[x]

    if len(candidate_containers) <= container_numbers:
        return candidate_containers

    util_max = max(artificial_utils.values())
    util_min = min(artificial_utils.values())
    print(artificial_utils)
    print(util_max, util_min)
    for x in artificial_utils:
        normalized = (artificial_utils[x] - util_min) / (util_max - util_min)
        scaled = normalized * 60 + 20
        artificial_utils[x] = scaled
    samples = {}
    for x in candidate_containers:
        if random.uniform(5, 95) > artificial_utils[x]:
            samples[x] = candidate_containers[x]
    diff = len(samples) - container_numbers
    keys = list(samples)
    data = {}
    if diff > 0:
        rng = np.random.default_rng()
        numbers = rng.choice(len(samples), len(samples) - diff, replace=False)
        for i in numbers:
            data[keys[i]] = samples[keys[i]]
        return data
    else:
        return samples


def calculate_delta_si(beta, delta_response, alpha, threshold):
    value = (beta / alpha) * min((delta_response / threshold), alpha)
    return value


def update_configurations(candidate_configs, current_configs, alpha, beta, threshold, delta_response):
    new_configs = {}
    random_exploration = 0.5
    delta_si = calculate_delta_si(beta, delta_response, alpha, threshold)
    for x in candidate_configs:
        new_configs[x] = round((current_configs[x] * (1 - delta_si)), 1)

    # randomly increase cpu for some containers. 80% of container will not change
    for x in current_configs:
        if x in new_configs:
            continue
        else:
            # if random.uniform(0, 1) > random_exploration:
            #     print(x, current_configs[x])
            #     new_configs[x] = round((current_configs[x] * (1 + delta_si)), 1)
            # else:
            new_configs[x] = round(current_configs[x], 1)
    return new_configs, delta_si


def get_poisson_rate(requests):
    # poisson = 48901 * requests**(-1*1.053)
    rps = [50, 100, 175, 225, 300, 350]
    poisson = [200, 110, 60, 50, 35, 25]
    x = np.array(rps)
    y = np.array(poisson)
    f = interp1d(x, y)
    poisson = f(np.array(requests))
    return int(poisson)


def get_response(rps, cost):
    return 0.1441 * (rps / cost) + 207.65
    # return 0.9806 * rps + 273.53


def apply_configurations(new_configs):
    pass


if __name__ == '__main__':
    SLO = 900
    ranges = {
        1: {"min": 50, "max": 100},
        2: {"min": 101, "max": 200},
        3: {"min": 201, "max": 225},
        4: {"min": 301, "max": 400},
        5: {'min': 250, 'max': 275},
        6: {'min': 225, 'max': 250},
        7: {'min': 275, 'max': 300}
    }

    ns_changed_total = 0

    alpha = 1
    beta = 0.3
    profile = 1
    experiment_no = 1
    number_of_containers = len(container_list)
    number_of_process = 2
    history = HistoryDB()
    HISTORY_WEIGHT = 1
    lower_bound = 1
    current_configurations = {}

    data_size = 60
    while data_size:
        data_size -= 1
        print("BEGIN EXPERIMENT: ", profile)
        range_id = 1
        rps = random.randint(201, 224)  # request_per_seconds.pop(0)
        #rps = 210
        for x in ranges:
            if ranges[x]["min"] <= rps < ranges[x]["max"]:
                range_id = x
                break

        rate = get_poisson_rate(rps)
        print("Predicted RPS is: ", rps)
        # apply_configurations(DEFAULT_CONFIGS)
        previous_data = history.get_last_configuration(SLO, range_id)
        # print(previous_data)
        configuration = DEFAULT_CONFIGS
        if previous_data:
            print("Got configs from DB...")
            # check if this there's new configuration
            if previous_data[0][12]:
                configuration = previous_data[0][12]
                print("Experiment ID: %s, Configs: %s" % (previous_data[0][1], configuration))
                apply_configurations(configuration)
            else:
                # get configuration from history..
                data = history.get_previous_history(SLO, range_id, previous_data[0][8])
                # print(data)
                if data:
                    configuration = data[0][15]
                    print("Experiment ID: %s, Configs: %s" % (data[0][1], configuration))
                    apply_configurations(configuration)
                else:
                    print("No configuration that matched criterias, applying default...")
                    apply_configurations(configuration)
        else:
            print("Applying default configs...")
            apply_configurations(configuration)

        current_settings = {"config_id": profile}
        config_name = str(profile) + "_"
        # main experiments
        print("Starting the main experiments for 2 minutes with poisson: ", rate)

        # BEGIN ALGORITHM PARTS
        start = time.time()

        if type(configuration) == str:
            current_configs = eval(configuration)
        else:
            current_configs = configuration

        utilizations, throttles = process_utlization(rps, current_configs, range_id)

        for x in utilizations:
            container_util_list[x].append(utilizations[x])

        config_cost = 0
        for c in current_configs:
            config_cost += current_configs[c]
        config_cost = config_cost * 0.00001124444 * EXPERIMENT_TIME

        percentile_95 = get_response(rps, config_cost)
        print("POISSON RATE IS: ", rate)
        print("RPS: %s, 95 Percentile Response: %s" % (rps, percentile_95))

        current_settings["experiment_id"] = profile
        current_settings["configs"] = current_configs
        current_settings["utils"] = utilizations
        current_settings["throttles"] = throttles
        current_settings["response"] = percentile_95
        current_settings["time"] = datetime.datetime.now()
        current_settings["rps"] = rps
        current_settings["delta_response"] = -1
        current_settings["slo"] = SLO
        current_settings["range_id"] = range_id
        current_settings["rps_range"] = ranges[range_id]
        current_settings["cost"] = config_cost
        current_settings["delta_si"] = -1
        current_settings["n_s"] = -1
        current_settings["threshold"] = -1
        current_settings["current_configs"] = current_configs
        current_settings["poisson"] = str(rate) + "x" + str(number_of_process)
        current_settings["container_stats"] = "N/A"

        # history.insert_into_table(current_settings)
        q_value = get_stopping_threshold(SLO, range_id, ranges[range_id], history, lower_bound)
        print("Q value is ", q_value)
        if q_value == -1:
            profile += 1
            print(current_settings)
            history.insert_into_table(current_settings)
            print("No changes in configs. Conducting same experiments...")
            print("######################")

            for x in utilizations:  # update limit of containers.
                max_value = max(container_util_list[x])
                if max_value > container_limits[x]:
                    container_limits[x] = max_value

            continue

        threshold = (((lower_bound * SLO - q_value) / (ranges[range_id]["max"] - ranges[range_id]["min"])) * (
                rps - ranges[range_id]["min"])) + q_value
        print("Threshold for RPS: %d is %d" % (rps, threshold))

        delta_response = threshold - percentile_95
        current_settings["delta_response"] = delta_response
        current_settings["threshold"] = threshold

        if percentile_95 > threshold:
            """
            select previous configuration that didn't violate SLO
            """
            print("Response time exceeded threshold. Will go back to history")
            print("current_settings: ", current_settings)
            current_settings["configs"] = ""
            history.insert_into_table(current_settings)
        else:
            for x in utilizations:  # update limit of containers.
                max_value = max(container_util_list[x])
                if max_value > container_limits[x]:
                    container_limits[x] = max_value

            # select_container_numbers = int((number_of_containers / alpha) * (delta_response / SLO))
            select_container_numbers = int((number_of_containers / alpha) * (delta_response / threshold))

            if select_container_numbers > number_of_containers:
                select_container_numbers = number_of_containers

            candidate_containers = choose_containers(select_container_numbers, utilizations, throttles,
                                                     current_configs, )
            # print("Selected Containers: ", candidate_containers)
            new_configs, delta_si = update_configurations(candidate_containers, current_configs, alpha, beta, threshold,
                                                          delta_response)

            current_settings["configs"] = new_configs
            current_settings["delta_si"] = delta_si
            current_settings["n_s"] = select_container_numbers
            print("n_s: ", current_settings["n_s"])
            print("Current configus: ", current_settings["current_configs"])
            print("New configs: ", current_settings["configs"])
            history.insert_into_table(current_settings)

            # CODE for dynamic range
            # if select_container_numbers < 3:
            #     ns_changed_total += 1
            #
            # if ns_changed_total == 3:
            #     available_range_id = 0
            #     for x in ranges:
            #         if available_range_id <= x:
            #             available_range_id = x
            #     available_range_id += 1
            #
            #     range_min = ranges[range_id]["min"]
            #     range_max = ranges[range_id]["max"]
            #
            #     if range_max - range_min < 45:
            #         continue
            #
            #     ranges[range_id]["min"] = range_min
            #     ranges[range_id]["max"] = range_min + int((range_max-range_min) / 2)
            #
            #     ranges[available_range_id] = {}
            #     ranges[available_range_id]["min"] = range_min + int((range_max-range_min) / 2)
            #     ranges[available_range_id]["max"] = range_max
            #
            #     save_q_value(SLO, available_range_id, q_value, QValueDB())
            #     current_settings["range_id"] = available_range_id
            #     current_settings["rps_range"] = ranges[available_range_id]
            #     history.insert_into_table(current_settings)

        end = time.time()
        duration = end - start
        print("Time to apply changes: ", duration)
        print("####################")
        profile += 1
    print("Final Limits: ", container_limits)
    # print(ranges)
