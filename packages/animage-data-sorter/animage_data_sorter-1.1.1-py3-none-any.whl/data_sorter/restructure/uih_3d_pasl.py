from ._dicom import *
from ._dicom_util import write_dicom_series
from .data_sorter_base import DataSorterASLBase


class DataSorterUIHPASL(DataSorterASLBase):
    def __init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, extra_factor, calc_c_cbf):
        DataSorterASLBase.__init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf)
        if extra_factor is None or extra_factor == 0:
            logger.debug('extra_factor 未设置')
            # raise Exception('extra_factor 未设置')
        else:
            self.extra_factor = 32 / extra_factor
        self.M0 = None
        self.CBF = None # CBF参数图
        self.Control = None
        self.Label = None

        self.M0_count = 0
        self.CBF_count = 0
        # 区别M0与灌注图
        for series in self.series_list:
            if not isinstance(series, SeriesModel):
                continue
            seriesDescription = series.SeriesDescription.lower().replace('-', ' ')
            if seriesDescription.find('m0') > -1:
                self.M0_count += 1
                self.M0 = series
            elif seriesDescription.find('cbf') > -1:
                self.CBF_count += 1
                self.CBF = series
            elif seriesDescription.find('ctrl') > -1:
                self.Control = series
            elif seriesDescription.find('tag') > -1:
                self.Label = series

    def validate_series(self):
        if self.M0 is None:
            raise MissingSequenceError('M0')
        if self.CBF is None:
            raise MissingSequenceError('CBF')

        if self.M0_count > 1:
            raise SeriesTooMany(f'发现{self.M0_count}组M0图像，请保留一组再进行处理')
        if self.CBF_count > 1:
            raise SeriesTooMany(f'发现{self.CBF_count}组CBF图像，请保留一组再进行处理')

    def Sorter(self):
        super(DataSorterUIHPASL, self).Sorter()

        self.validate_series()

        # self.generate_calc_cbf_3d_pasl()
        self.generate_cbf_3d_pasl()

    def generate_cbf_3d_pasl(self):
        self.M0: SeriesModel
        m0_image = self.M0.load()
        # 多张M0只有第一张有效
        m0_image = m0_image[...,0]
        write_dicom_series(m0_image, self.M0, 'asl-m0', 1001, os.path.join(self.output_root, 'asl', 'm0'))

        self.CBF: SeriesModel
        cbf_image = self.CBF.load()
        cbf_image = cbf_image[...,0]
        # todo M0与CBF分辨率不一致时
        # if cbf_image.shape != m0_image.shape:
        #     raise SpaceIsDifferentError('CBF', 'M0')
        write_dicom_series(cbf_image * 10, self.CBF, 'asl-cbf1', 1002, os.path.join(self.output_root, 'asl', 'cbf1'),
                           slope=0.1)

    def generate_calc_cbf_3d_pasl(self):
        self.M0: SeriesModel
        m0_image = self.M0.load()
        # 多张M0只有第一张有效
        m0_image = m0_image[:,:,:,0]
        write_dicom_series(m0_image, self.M0, 'asl-m0', 1001, os.path.join(self.output_root, 'asl', 'm0'))

        control = self.Control.load()
        label = self.Label.load()
        repetitions = control.shape[-1]
        pwi = np.zeros(m0_image.shape)
        sub = control - label
        for i in range(repetitions):
            pwi += sub[:,:,:,i]
        pwi /= repetitions

        # calculate CBF
        t_inv = self.delay_time  # sec, inversion time
        l_dur = self.label_dur  # sec, labeling duration
        bb_p = 0.9  # mL/g, blood-brain partition coefficient
        t1_b = 1.65  # sec, relaxation of blood at 3.0T
        lab_eff = 0.98  # labeling efficiency for PASL
        u_cnv = 6000  # units conversion from mL/g/s to mL/100g/min

        upper_param = u_cnv * bb_p * np.exp(t_inv / t1_b)
        lower_param = 2 * lab_eff * l_dur
        calc_cbf = pwi / m0_image.astype(float) * upper_param / lower_param
        write_dicom_series(calc_cbf * 10, self.M0, 'asl-cbf1', 1002, os.path.join(self.output_root, 'asl', 'cbf1'),
                           slope=0.1)

    def _gen_mask(self, input_image):
        threshold = 0.5 * np.sum(np.multiply(input_image, input_image)) / np.sum(input_image)
        output_image = np.zeros(np.shape(input_image))
        output_image[input_image >= threshold] = 1
        return output_image