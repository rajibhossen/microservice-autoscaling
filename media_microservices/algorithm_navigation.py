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
from data_processing import end_to_end, process_utlization, get_current_configs

import client
from metrics_collection.prometheus_data import get_resource_utilization, get_container_settings
from utils.navigation_slo_threshold import get_stopping_threshold
from utils.db_utils import HistoryDB

container_list = ['compose-review-service', 'movie-id-service', 'movie-review-service', 'nginx-web-server',
                  'rating-service',
                  'text-service', 'user-service']
EXPERIMENT_TIME = 120  # seconds
THROTTLE_PERCENTAGE = 0.001  # 1%
DEFAULT_CONFIGS = {'compose-review-service': 4, 'movie-id-service': 4, 'movie-review-service': 4,
                   'nginx-web-server': 5, 'rating-service': 4, 'text-service': 4, 'user-service': 4}
default = 10
container_limits = {'compose-review-service': default, 'movie-id-service': default, 'movie-review-service': default,
                    'nginx-web-server': default, 'rating-service': default, 'text-service': default,
                    'user-service': default}

container_throttle_limits = {'compose-review-service': 0, 'movie-id-service': 0, 'movie-review-service': 0,
                             'nginx-web-server': 0, 'rating-service': 0, 'text-service': 0, 'user-service': 0}

container_util_list = {'compose-review-service': [], 'movie-id-service': [], 'movie-review-service': [],
                       'nginx-web-server': [], 'rating-service': [], 'text-service': [], 'user-service': []}
request_per_seconds = [634, 633, 633, 632, 631, 630, 629, 623, 618, 606, 595, 577, 559, 534, 514, 489, 470, 448, 433,
                       417, 408, 400, 396, 394, 394, 396, 399, 404, 407, 414, 419, 428, 435, 448, 460, 478, 493, 512,
                       527, 544, 555, 574, 587, 613, 635, 662, 687, 716, 736, 758, 767, 776, 781, 786, 788, 791, 793,
                       797, 801, 806, 812, 819, 824, 831, 837, 843, 848, 853, 856, 859, 861, 863, 864, 866, 866, 864,
                       861, 854, 846, 832, 819, 801, 786, 771, 760, 751, 746, 743, 744, 746, 749, 752, 754, 756, 757,
                       756, 754, 748, 742, 730, 719, 701, 687, 666, 648, 624, 605, 580, 561, 534, 514, 490, 472, 451,
                       436, 420, 410, 402, 399, 396, 396, 397, 400, 403, 406, 411, 415, 423, 429, 441, 452, 470, 486,
                       509, 529, 556, 578, 606, 627, 652, 671, 693, 708, 726, 738, 751, 760, 769, 774, 780, 783, 787,
                       790, 793, 796, 799, 802, 805, 807, 810, 812, 814, 816, 819, 821, 823, 825, 827, 828, 830, 831,
                       829, 828, 822, 816, 805, 795, 779, 766, 752, 742, 733, 727, 722, 722, 720, 720, 721, 722, 722,
                       723, 722, 722, 721, 717, 710, 703, 690, 678, 659, 643, 620, 600, 574, 554, 528, 509, 484, 466,
                       444, 430, 412, 402, 392, 388, 384, 384, 384, 387, 391, 394, 399, 403, 411, 418, 429, 439, 456,
                       471, 494, 512, 539, 562, 591, 614, 642, 663, 688, 705, 724, 737, 752, 762, 772, 777, 783, 785,
                       788, 787, 787, 787, 788, 790, 793, 797, 802, 806, 811, 815, 820, 824, 828, 830, 833, 835, 837,
                       839, 839, 838, 833, 827, 816, 805, 789, 774, 754, 739, 724, 714, 706, 704, 703, 707, 713, 719,
                       725, 729, 730, 729, 726, 722, 714, 707, 693, 682, 665, 650, 628, 610, 585, 565, 539, 519, 494,
                       474, 452, 437, 419, 407, 398, 395, 392, 391, 391, 393, 397, 398, 401, 403, 409, 415, 425, 433,
                       449, 463, 484, 502, 527, 549, 579, 603, 630, 651, 676, 693, 713, 724, 738, 748, 758, 763, 769,
                       772, 775, 775, 776, 777, 779, 782, 785, 788, 793, 796, 801, 805, 809, 813, 816, 818, 821, 822,
                       824, 825, 826, 826, 821, 816, 806, 795, 780, 765, 744, 729, 715, 705, 696, 692, 688, 690, 692,
                       693, 695, 696, 696, 697, 694, 692, 687, 681, 671, 660, 644, 631, 611, 594, 570, 551, 526, 506,
                       481, 463, 441, 426, 408, 397, 384, 377, 370, 367, 365, 365, 366, 367, 370, 372, 377, 382, 390,
                       397, 410, 423, 442, 459, 483, 504, 532, 555, 583, 603, 629, 646, 666, 678, 692, 701, 711, 718,
                       724, 728, 731, 732, 731, 729, 727, 724, 723, 722, 722, 723, 724, 724, 725, 726, 726, 726, 726,
                       726, 725, 724, 722, 720, 715, 709, 700, 691, 677, 664, 646, 630, 612, 597, 579, 567, 553, 545,
                       536, 530, 525, 523, 521, 521, 522, 523, 524, 525, 523, 521, 517, 512, 504, 496, 484, 475, 462,
                       451, 437, 425, 410, 398, 383, 372, 359, 349, 337, 330, 322, 317, 314, 312, 311, 312, 314, 316,
                       320, 323, 329, 334, 343, 352, 364, 375, 389, 401, 417, 430, 448, 462, 480, 494, 511, 525, 541,
                       552, 566, 575, 585, 592, 600, 605, 610, 613, 617, 620, 623, 625, 627, 628, 631, 632, 635, 637,
                       640, 644, 648, 651, 653, 655, 654, 652, 648, 642, 634, 627, 617, 609, 598, 589, 578, 570, 561,
                       554, 547, 543, 540, 539, 538, 539, 540, 542, 543, 544, 544, 543, 539, 535, 529, 523, 513, 505,
                       493, 484, 471, 460, 445, 433, 418, 406, 392, 381, 369, 360, 351, 345, 339, 337, 335, 336, 338,
                       340, 345, 348, 354, 359, 367, 375, 386, 396, 411, 424, 441, 455, 474, 488, 507, 521, 539, 552,
                       569, 582, 597, 608, 623, 633, 646, 655, 667, 676, 687, 696, 707, 716, 725, 731, 738, 743, 747,
                       749, 749, 748, 749, 749, 748, 748, 747, 747, 746, 743, 738, 733, 725, 718, 709, 702, 697, 695,
                       692, 694, 694, 696, 698, 698, 698, 697, 696, 696, 695, 695, 693, 691, 683, 676, 663, 649, 629,
                       611, 585, 566, 540, 521, 496, 478, 456, 441, 424, 412, 400, 394, 389, 387, 386, 388, 391, 394,
                       397, 400, 406, 412, 421, 429, 443, 457, 477, 493, 518, 539, 568, 591, 619, 641, 667, 685, 706,
                       720, 737, 749, 761, 769, 778, 784, 791, 795, 801, 806, 812, 817, 824, 829, 836, 841, 847, 851,
                       857, 860, 865, 868, 872, 874, 877, 880, 880, 879, 873, 866, 854, 841, 824, 809, 789, 774, 760,
                       751, 744, 741, 738, 739, 740, 740, 739, 737, 735, 732, 728, 724, 718, 713, 702, 692, 675, 661,
                       640, 621, 595, 574, 547, 526, 499, 480, 457, 442, 424, 412, 399, 392, 386, 383, 381, 382, 385,
                       388, 393, 396, 404, 410, 420, 428, 443, 458, 479, 497, 524, 547, 578, 602, 631, 653, 679, 697,
                       717, 730, 745, 755, 766, 773, 782, 788, 795, 800, 806, 811, 816, 820, 824, 827, 831, 834, 838,
                       841, 845, 849, 852, 854, 856, 856, 856, 856, 854, 853, 848, 844, 835, 826, 812, 798, 778, 762,
                       747, 737, 727, 723, 719, 720, 722, 723, 724, 725, 725, 726, 724, 721, 716, 712, 702, 692, 677,
                       665, 645, 628, 603, 583, 557, 536, 509, 489, 465, 449, 431, 418, 404, 396, 390, 387, 384, 384,
                       384, 385, 389, 391, 397, 404, 414, 423, 440, 453, 475, 493, 519, 541, 571, 595, 624, 646, 672,
                       690, 713, 727, 745, 758, 772, 781, 790, 796, 802, 804, 807, 808, 811, 814, 818, 822, 827, 830,
                       835, 838, 842, 844, 846, 848, 849, 850, 851, 851, 851, 852, 848, 845, 837, 829, 816, 802, 784,
                       769, 749, 733, 721, 715, 708, 708, 707, 712, 717, 717, 717, 718, 716, 714, 709, 705, 696, 688,
                       674, 663, 645, 630, 608, 590, 565, 545, 520, 500, 476, 459, 439, 427, 411, 402, 391, 385, 379,
                       376, 375, 375, 379, 383, 390, 397, 408, 417, 432, 445, 466, 483, 508, 529, 559, 584, 615, 639,
                       667, 687, 711, 725, 743, 754, 768, 777, 787, 792, 797, 799, 802, 803, 805, 807, 810, 813, 817,
                       820, 824, 827, 830, 833, 836, 838, 840, 841, 841, 840, 839, 837, 833, 830, 822, 814, 802, 790,
                       773, 759, 741, 728, 713, 704, 694, 690, 685, 684, 682, 682, 680, 679, 676, 673, 669, 666, 660,
                       656, 646, 637, 623, 610, 590, 572, 548, 528, 503, 484, 460, 444, 425, 412, 392, 378, 369, 364,
                       360, 358, 356, 361, 368, 369, 372, 375, 382, 388, 399, 409, 426, 440, 462, 480, 506, 528, 558,
                       581, 607, 626, 649, 664, 681, 691, 703, 712, 721, 726, 731, 733, 735, 734, 732, 731, 729, 728,
                       727, 727, 727, 728, 728, 728, 727, 727, 726, 724, 723, 722, 721, 721, 720, 719, 715, 711, 704,
                       697, 685, 675, 659, 647, 630, 616, 599, 586, 571, 561, 550, 543, 537, 534, 530, 529, 527, 526,
                       524, 522, 519, 516, 512, 508, 501, 494, 483, 474, 461, 450, 435, 423, 408, 397, 383, 372, 360,
                       352, 342, 335, 328, 325, 322, 321, 320, 322, 326, 329, 334, 338, 347, 354, 365, 375, 389, 402,
                       419, 432, 451, 465, 485, 499, 517, 531, 547, 558, 572, 581, 591, 598, 607, 612, 618, 622, 627,
                       630, 634, 637, 640, 643, 646, 648, 650, 652, 653, 654, 655, 655, 655, 655, 655, 654, 652, 650,
                       646, 643, 637, 632, 623, 615, 606, 598, 588, 581, 574, 570, 567, 566, 565, 566, 567, 568, 569,
                       570, 571, 571, 568, 566, 560, 554, 545, 536, 524, 515, 501, 491, 477, 466, 451, 440, 425, 414,
                       401, 391, 379, 371, 364, 360, 357, 357, 357, 359, 362, 365, 369, 371, 377, 382, 390, 397, 408,
                       419, 433, 446, 464, 478, 498, 513, 533, 548, 566, 579, 596, 608, 623, 634, 647, 657, 669, 677,
                       687, 694, 704, 712, 721, 729, 738, 745, 753, 758, 765, 770, 776, 781, 785, 788, 790, 790, 790,
                       788, 785, 783, 778, 774, 765, 758, 753, 748, 744, 743, 735, 729, 716, 707, 694, 682, 666, 650,
                       649, 647, 642, 632, 611, 602, 587, 557, 536, 510, 492, 477, 455, 446, 434, 424, 411, 399, 397,
                       391, 384, 390, 392, 400, 412, 422, 428, 443, 456, 468, 491, 500, 507, 526, 545, 555, 570, 571,
                       596, 629, 665, 690, 720, 753, 779, 793, 794, 795, 794, 790, 785, 794, 809, 824, 828, 834, 837,
                       834, 839, 845, 848, 860, 859, 875, 881, 866, 865, 862, 843, 862, 852, 856, 854, 842, 827, 823,
                       792, 777, 755, 755, 737, 745, 751, 750, 750, 752, 744, 746, 737, 736, 742, 739, 745, 754, 741,
                       738, 709, 690, 673, 648, 611, 593, 563, 543, 514, 497, 471, 455, 441, 418, 413, 411, 398, 394,
                       386, 386, 395, 396, 393, 405, 413, 418, 420, 423, 437, 445, 455, 473, 507, 523, 558, 566, 597,
                       616, 647, 662, 692, 707, 725, 749, 767, 757, 757, 756, 747, 763, 748, 749, 763, 768, 779, 787,
                       796, 797, 801, 801, 805, 794, 806, 800, 819, 826, 825, 823, 832, 834, 823, 813, 790, 780, 781,
                       780, 768, 772, 762, 755, 747, 742, 736, 730, 724, 715, 730, 749, 742, 733, 729, 728, 740, 739,
                       715, 713, 698, 679, 651, 628, 596, 583, 557, 545, 528, 514, 487, 466, 451, 430, 415, 402, 391,
                       390, 384, 373, 381, 385, 393, 403, 408, 421, 436, 434, 441, 451, 456, 470, 488, 497, 527, 556,
                       584, 619, 655, 673, 711, 736, 748, 758, 772, 773, 779, 774, 769, 763, 770, 756, 755, 764, 774,
                       776, 780, 773, 778, 789, 790, 795, 801, 811, 816, 819, 814, 816, 814, 823, 830, 842, 846, 852,
                       843, 827, 806, 788, 762, 744, 720, 703, 696, 681, 688, 694, 710, 715, 727, 735, 748, 739, 735,
                       716, 715, 712, 695, 679, 658, 635, 618, 600, 568, 545, 522, 501, 480, 459, 434, 420, 409, 400,
                       397, 397, 397, 389, 392, 391, 397, 395, 398, 400, 409, 415, 432, 433, 458, 473, 488, 513, 541,
                       558, 588, 602, 618, 646, 669, 684, 700, 723, 738, 765, 766, 767, 776, 785, 779, 785, 782, 799,
                       799, 798, 805, 810, 813, 819, 822, 820, 823, 807, 807, 818, 802, 810, 813, 812, 817, 809, 793,
                       793, 764, 761, 743, 732, 722, 709, 698, 695, 684, 680, 674, 667, 659, 666, 670, 678, 688, 690,
                       689, 688, 676, 675, 668, 653, 635, 628, 614, 598, 569, 537, 509, 501, 479, 466, 449, 431, 420,
                       408, 393, 378, 368, 358, 358, 356, 354, 355, 364, 365, 372, 374, 384, 395, 407, 421, 440, 455,
                       480, 504, 529, 553, 577, 607, 641, 654, 679, 698, 703, 705, 706, 702, 722, 726, 728, 747, 758,
                       759, 765, 764, 746, 748, 741, 735, 742, 727, 713, 730, 723, 721, 731, 721, 733, 745, 728, 729,
                       722, 711, 705, 694, 671, 671, 658, 649, 635, 620, 596, 590, 565, 554, 547, 529, 520, 528, 523,
                       528, 516, 512, 520, 527, 515, 518, 509, 512, 508, 506, 497, 491, 477, 466, 455, 440, 414, 398,
                       389, 379, 371, 359, 344, 336, 327, 315, 305, 301, 300, 307, 310, 313, 324, 327, 336, 336, 346,
                       356, 373, 383, 403, 406, 423, 428, 440, 452, 472, 481, 499, 518, 543, 563, 567, 569, 585, 598,
                       612, 607, 616, 623, 623, 615, 622, 613, 617, 609, 610, 613, 622, 629, 633, 646, 648, 662, 674,
                       683, 675, 668, 655, 658, 635, 615, 594, 592, 588, 586, 571, 576, 575, 578, 558, 549, 543, 542,
                       528, 526, 519, 525, 526, 519, 522, 530, 524, 529, 518, 512, 507, 501, 484, 485, 464, 454, 445,
                       431, 415, 413, 394, 385, 374, 361, 355, 341, 329, 326, 321, 323, 328, 331, 340, 350, 356, 363,
                       375, 385, 401, 414, 423, 437, 463, 479, 493, 499, 515, 528, 551, 557, 579, 595, 617, 635, 660,
                       669, 676, 684, 692, 693, 697, 705, 710, 720, 720, 721, 728, 726, 730, 729, 724, 722, 737, 735,
                       747, 740, 735, 746, 744, 738, 743, 731, 716, 709, 695, 695, 692, 688, 682, 683, 686, 696, 687,
                       680, 686, 698, 705, 715, 715, 727, 729, 714, 699, 693, 679, 653, 625, 611, 594, 575, 549, 529,
                       509, 497, 463, 444, 425, 415, 396, 397, 395, 396, 396, 398, 396, 401, 398, 391, 398, 399, 408,
                       419, 430, 450, 481, 503, 531, 555, 581, 607, 622, 645, 657, 675, 691, 706, 736, 765, 759, 782,
                       792, 797, 811, 812, 821, 830, 838, 839, 847, 852, 847, 838, 841, 841, 857, 858, 851, 863, 881,
                       898, 887, 883, 891, 894, 874, 850, 844, 848, 841, 819, 793, 790, 778, 758, 752, 747, 745, 757,
                       750, 748, 744, 724, 723, 727, 712, 713, 717, 713, 707, 692, 677, 671, 652, 632, 608, 590, 552,
                       528, 494, 469, 438, 423, 402, 396, 378, 374, 368, 370, 371, 373, 373, 378, 381, 388, 389, 391,
                       408, 420, 436, 454, 479, 496, 523, 551, 583, 611, 643, 657, 693, 707, 722, 736, 747, 746, 772,
                       774, 788, 795, 804, 809, 813, 813, 829, 829, 834, 842, 847, 860, 859, 843, 841, 831, 824, 838,
                       840, 851, 850, 854, 873, 861, 838, 837, 824, 828, 819, 804, 801, 797, 780, 770, 767, 773, 768,
                       760, 749, 751, 738, 720, 717, 709, 708, 716, 712, 716, 715, 700, 679, 665, 639, 612, 590, 574,
                       551, 534, 508, 495, 480, 456, 431, 420, 412, 405, 400, 392, 387, 387, 379, 376, 379, 378, 379,
                       388, 400, 418, 431, 448, 471, 493, 513, 530, 551, 584, 617, 630, 668, 691, 728, 746, 748, 747,
                       773, 771, 777, 784, 793, 800, 817, 807, 804, 808, 805, 815, 831, 823, 821, 823, 839, 845, 828,
                       835, 835, 848, 854, 844, 829, 835, 815, 814, 817, 802, 798, 792, 781, 781, 759, 736, 733, 711,
                       707, 702, 700, 716, 713, 718, 729, 737, 744, 731, 722, 728, 724, 719, 698, 680, 672, 653, 623,
                       594, 567, 541, 512, 486, 469, 453, 434, 416, 405, 394, 379, 373, 369, 372, 372, 372, 375, 378,
                       381, 385, 393, 403, 424, 442, 462, 484, 504, 521, 547, 573, 594, 629, 649, 671, 686, 697, 703,
                       717, 735, 745, 751, 773, 790, 801, 807, 803, 804, 810, 803, 796, 802, 814, 802, 807, 809, 825,
                       841, 836, 837, 854, 859, 876, 871, 864, 854, 855, 836, 826, 799, 786, 775, 776, 756, 740, 730,
                       724, 706, 697, 683, 669, 671, 660, 652, 650, 647, 640, 634, 626, 633, 639, 626, 619, 606, 595,
                       587, 559, 525, 508, 473, 455, 433, 409, 393, 386, 370, 366, 360, 357, 360, 363, 357, 363, 362,
                       363, 369, 373, 380, 385, 390, 399, 418, 439, 454, 469, 494, 526, 563, 589, 618, 631, 661, 682,
                       691, 687, 701, 709, 732, 739, 741, 742, 750, 738, 718, 707, 693, 689, 691, 695, 692, 696, 700,
                       703, 714, 712, 716, 731, 742, 738, 743, 729, 733, 719, 698, 680, 668, 665, 663, 654, 648, 648,
                       637, 638, 612, 593, 578, 569, 552, 551, 538, 529, 532, 523, 518, 519, 512, 506, 516, 507, 503,
                       494, 491, 485, 486, 470, 464, 451, 439, 422, 406, 393, 376, 369, 364, 357, 343, 337, 325, 320,
                       317, 311, 309, 315, 320, 320, 327, 328, 344, 354, 368, 372, 386, 404, 415, 417, 437, 447, 468,
                       493, 509, 526, 547, 552, 564, 583, 595, 604, 610, 618, 624, 626, 628, 631, 634, 648, 645, 650,
                       659, 665, 653, 651, 648, 650, 648, 648, 637, 638, 644, 640, 645, 643, 641, 633, 633, 616, 611,
                       605, 599, 592, 594, 589, 587, 574, 564, 557, 554, 554, 554, 562, 569, 576, 585, 579, 574, 569,
                       552, 542, 528, 524, 517, 505, 491, 485, 479, 466, 440, 429, 414, 408, 391, 381, 376, 374, 364,
                       362, 358, 363, 364, 365, 372, 374, 382, 377, 381, 383, 392, 392, 410, 422, 444, 460, 476, 486,
                       514, 531, 551, 556, 564, 578, 603, 604, 621, 630, 655, 679, 696, 691, 697, 692, 704, 699, 696,
                       697, 711, 718, 733, 725, 732, 749, 752, 753, 773, 787, 808, 817, 806, 803, 809, 801, 778, 774,
                       760, 752, 747, 731, 731, 743, 717, 699, 687, 680, 669, 653, 623, 624, 625, 627, 614, 618, 605,
                       603, 586, 570, 541, 526, 494, 471, 444, 428, 419, 410, 400, 401, 397, 405, 403, 402, 406, 410,
                       416, 427, 429, 431, 438, 453, 471, 487, 503, 527, 553, 566, 596, 606, 628, 653, 681, 698, 731,
                       736, 760, 766, 762, 762, 780, 781, 784, 782, 777, 779, 771, 768, 778, 786, 804, 824, 851, 866,
                       870, 879, 889, 891, 900, 883, 887, 887, 880, 868, 858, 829, 817, 810, 798, 781, 764, 743, 735,
                       746, 740, 735, 747, 765, 774, 778, 764, 766, 762, 754, 735, 734, 722, 721, 689, 687, 663, 648,
                       618, 614, 585, 567, 534, 511, 487, 473, 446, 426, 420, 413, 401, 403, 401, 399, 406, 404, 403,
                       405, 413, 418, 427, 433, 452, 462, 481, 498, 519, 534, 551, 561, 584, 617, 641, 649, 675, 703,
                       723, 742, 742, 740, 750, 761, 758, 760, 761, 764, 770, 783, 787, 795, 806, 804, 809, 806, 813,
                       805, 817, 808, 817, 818, 828, 822, 818, 809, 810, 815, 818, 803, 789, 785, 767, 762, 744, 729,
                       734, 730, 734, 735, 741, 740, 732, 731, 738, 739, 747]


def run_program(rate, experiment_time, experiment_no, threads):
    procs = []
    # two process, 1,2
    # params - script name, rate, runtime (s), log file name
    # print(threads)
    for i in range(1, threads):
        p = sp.Popen(
            [sys.executable, "load_test.py", rate, experiment_time,
             experiment_no + "/data_p" + rate + "_t" + str(threads) + "_" + str(i)])
        procs.append(p)

    for p in procs:
        p.wait()


def collect_metrics():
    container_data = []
    for container in container_list:
        container_data.append(get_resource_utilization(container, int(EXPERIMENT_TIME / 60)))
        # print(get_resource_utilization(container))
    return container_data


def choose_containers(container_numbers, utilizations, throttles, current_configs):
    candidate_containers = {}
    for x in utilizations:
        if throttles[x] > THROTTLE_PERCENTAGE * EXPERIMENT_TIME:
            continue
        if current_configs[x] <= 0.3:
            continue
        candidate_containers[x] = utilizations[x]

    artificial_utils = {}
    for x in candidate_containers.keys():
        artificial_utils[x] = candidate_containers[x] / container_limits[x]
    print("ARTIFICIAL UTILS: ", artificial_utils)
    if len(candidate_containers) < container_numbers:
        return candidate_containers

    util_max = max(artificial_utils.values())
    util_min = min(artificial_utils.values())
    if util_max == util_min:
        for x in artificial_utils:
            scaled = artificial_utils[x] * 60 + 20
            artificial_utils[x] = scaled
    else:
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


def update_configurations(candidate_configs, current_configs, alpha, beta, threshold, delta_response,
                          random_exploration=0.0):
    new_configs = {}
    delta_si = calculate_delta_si(beta, delta_response, alpha, threshold)
    if random.uniform(0, 1) < random_exploration:
        for x in candidate_configs:
            new_configs[x] = max(DEFAULT_CONFIGS[x], round((current_configs[x] * (1 + delta_si)), 1))

        for x in current_configs:
            if x not in new_configs:
                new_configs[x] = round(current_configs[x], 1)
    else:
        for x in candidate_configs:
            new_configs[x] = round((current_configs[x] * (1 - delta_si)), 1)

        for x in current_configs:
            if x not in new_configs:
                new_configs[x] = round(current_configs[x], 1)
    return new_configs, delta_si


def avoid_cold_start():
    path = "load_data/algorithm_navigation/temps"

    if not os.path.exists(path):
        os.makedirs(path)

    run_program(str(45), str(60), "temps", 3)
    sp.call(['sh', './flush_db.sh'])


def get_poisson_rate(requets):
    # poisson = 48901 * requests**(-1*1.053)
    rps = [365.8583333, 308.5833333, 267.8916667, 236.9166667, 213.6166667, 193.0083333, 174.1, 161.3083333, 148.75,
           137.925, 128.1833333, 120.8583333, 114.0916667, 107.7916667, 101.75, 98.225, 81.71666667, 68.95, 61.80833333]
    poisson = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 120, 140, 160]

    x = np.array(rps)
    y = np.array(poisson)
    f = interp1d(x, y)
    poisson = f(np.array(requets))
    return int(poisson)


def apply_configurations(new_configs):
    if type(new_configs) == str:
        new_configs = eval(new_configs)

    for x in new_configs:
        settings = get_container_settings(x, 1)
        # cpu = float(new_configs[x]) / len(container_settings[x])
        cpu = round(float(new_configs[x]) / len(settings), 2)
        threads = []
        print(settings)
        for info in settings:
            print(x, info["node"], cpu, info["id"])
            # client.apply_actions(info["id"], info["node"], int(cpu * 100000))
            threads.append(
                threading.Thread(target=client.apply_cpu_resource, args=(info["id"], info["node"], int(cpu * 100000))))
            # client.apply_cpu_resource(info["id"], info["node"], int(cpu * 100000))
        for i in threads:
            i.start()
        for i in threads:
            i.join()


if __name__ == '__main__':
    SLO = 20

    ranges = {
        1: {"min": 100, "max": 150},
        2: {"min": 151, "max": 200},
        3: {"min": 201, "max": 250},
        4: {"min": 251, "max": 300},
        5: {"min": 301, "max": 350},
        6: {"min": 351, "max": 400},
        7: {"min": 401, "max": 450},
        8: {"min": 451, "max": 500}
    }

    alpha = 0.5
    beta = 0.2
    profile = 1
    experiment_no = 1
    number_of_containers = 7
    number_of_process = 10
    history = HistoryDB()
    HISTORY_WEIGHT = 1
    lower_bound = 1
    current_configurations = {}

    avoid_cold_start()
    # avoid_cold_start()
    # avoid_cold_start()

    data_size = 40
    rps_array = [105, 110, 115, 120, 125, 130, 135, 140, 145, 150]
    while data_size:
        data_size -= 1
        print("BEGIN EXPERIMENT: ", profile)
        range_id = 6
        # RPS = 100
        # RPS = request_per_seconds.pop(0)
        if rps_array:
            RPS = rps_array.pop(random.randrange(len(rps_array)))
        else:
            RPS = random.randint(105, 145)

        # RPS = random.randint(605, 695)
        # RPS = 650

        for x in ranges:
            if ranges[x]["min"] <= RPS < ranges[x]["max"]:
                range_id = x
                break

        rate = get_poisson_rate(RPS)

        print("Predicted RPS is: ", RPS)

        previous_data = history.get_last_configuration(SLO, range_id)
        # print(previous_data)
        if previous_data:
            print("Got configs from DB...")
            # check if this there's new configuration
            if previous_data[0][12]:
                print("Experiment ID: %s, Configs: %s" % (previous_data[0][1], previous_data[0][12]))
                apply_configurations(previous_data[0][12])
            else:
                # get configuration from history..
                data = history.get_previous_history(SLO, range_id, previous_data[0][8])
                # print(data)
                if data:
                    print("Experiment ID: %s, Configs: %s" % (data[0][1], data[0][15]))
                    apply_configurations(data[0][15])
                else:
                    print("No configuration that matched criterias, applying default...")
                    apply_configurations(DEFAULT_CONFIGS)
        else:
            print("Applying default configs...")
            apply_configurations(DEFAULT_CONFIGS)

        current_settings = {"config_id": profile}
        config_name = str(profile) + "_"
        path = "load_data/algorithm_navigation/" + config_name + str(experiment_no)

        if not os.path.exists(path):
            os.makedirs(path)

        # main experiments
        print("Starting the main experiments for 2 minutes with poisson: ", rate)
        run_program(str(rate), str(EXPERIMENT_TIME), config_name + str(experiment_no), number_of_process + 1)

        print("Collecting metrics....")
        metrics = collect_metrics()
        with open(path + "/p" + str(rate) + ".txt", 'w') as filehandle:
            json.dump(metrics, filehandle)

        # flashing databases
        sp.call(['sh', './flush_db.sh'])

        # BEGIN ALGORITHM PARTS
        start = time.time()
        rpss, responses = end_to_end(profile)
        percentile_95 = sum(responses) / len(responses)
        rps = sum(rpss) / len(rpss)
        print("POISSON RATE IS: ", rate)
        print("RPS: %s, 95 Percentile Response: %s" % (rps, percentile_95))
        utilizations, throttles = process_utlization(profile)

        for x in utilizations:
            utilizations[x] = sum(utilizations[x]) / len(utilizations[x])

        for x in throttles:
            throttles[x] = sum(throttles[x]) / len(throttles[x])

        for x in utilizations:
            container_util_list[x].append(utilizations[x])
        current_configs, container_settings = get_current_configs(profile)

        config_cost = 0
        for c in current_configs:
            config_cost += current_configs[c]
        config_cost = config_cost * 0.00001124444 * EXPERIMENT_TIME
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
        current_settings["container_stats"] = "None"  # container_stats

        q_value = get_stopping_threshold(SLO, range_id, ranges[range_id], history, lower_bound)
        print("Q value is ", q_value)
        if q_value == -1:
            profile += 1
            print(current_settings)
            history.insert_into_table(current_settings)
            print("No changes in configs. Conducting same experiments...")
            print("######################")
            continue

        threshold = (((lower_bound * SLO - q_value) / (ranges[range_id]["max"] - ranges[range_id]["min"])) * (
                rps - ranges[range_id]["min"])) + q_value
        print("Threshold for RPS: %d is %d" % (rps, threshold))

        delta_response = max(0, threshold - percentile_95)
        current_settings["delta_response"] = delta_response
        current_settings["threshold"] = threshold

        if percentile_95 > threshold:
            """
            select previous configuration that didn't violate SLO
            """
            print("Response time exceeded threshold. Will go back to history")
            print(current_settings)
            current_settings["configs"] = ""
            history.insert_into_table(current_settings)

        else:
            for x in utilizations:  # update limit of containers.
                max_value = max(container_util_list[x])
                if max_value > container_limits[x]:
                    container_limits[x] = max_value

            for x in throttles:  # update throttle of containers
                if throttles[x] >= container_throttle_limits[x]:
                    container_throttle_limits[x] = throttles[x]
            # select_container_numbers = int((number_of_containers / alpha) * (delta_response / SLO))
            select_container_numbers = int((number_of_containers / alpha) * (delta_response / threshold))

            if select_container_numbers > number_of_containers:
                select_container_numbers = number_of_containers

            candidate_containers = choose_containers(select_container_numbers, utilizations, throttles, current_configs)

            # random_explore = 1 - ((number_of_containers - select_container_numbers) / number_of_containers)
            # random_explore = 0.2
            # random_explore = delta_response / (alpha * SLO* (profile-10))
            new_configs, delta_si = update_configurations(candidate_containers, current_configs, alpha, beta, threshold,
                                                          delta_response, random_exploration=0)

            current_settings["configs"] = new_configs
            current_settings["delta_si"] = delta_si
            current_settings["n_s"] = select_container_numbers
            print("N_s: ", current_settings["n_s"], "Threshold: ", current_settings["threshold"])
            print("New configs: ", current_settings["configs"])
            history.insert_into_table(current_settings)

        end = time.time()
        duration = end - start
        print("Time to apply changes: ", duration)
        print("####################")
        profile += 1
