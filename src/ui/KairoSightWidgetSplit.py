# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'KairoSightWidgetSplit.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WidgetSplit(object):
    def setupUi(self, WidgetSplit):
        WidgetSplit.setObjectName("WidgetSplit")
        WidgetSplit.resize(270, 236)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WidgetSplit.sizePolicy().hasHeightForWidth())
        WidgetSplit.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(WidgetSplit)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_3 = QtWidgets.QGroupBox(WidgetSplit)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.formLayout_lockDimensions = QtWidgets.QFormLayout()
        self.formLayout_lockDimensions.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_lockDimensions.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_lockDimensions.setSpacing(0)
        self.formLayout_lockDimensions.setObjectName("formLayout_lockDimensions")
        self.lockDimensionsLabel = QtWidgets.QLabel(self.groupBox_3)
        self.lockDimensionsLabel.setObjectName("lockDimensionsLabel")
        self.formLayout_lockDimensions.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lockDimensionsLabel)
        self.lockDimensionsCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.lockDimensionsCheckBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lockDimensionsCheckBox.setChecked(True)
        self.lockDimensionsCheckBox.setObjectName("lockDimensionsCheckBox")
        self.formLayout_lockDimensions.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lockDimensionsCheckBox)
        self.horizontalLayout_3.addLayout(self.formLayout_lockDimensions)
        self.formLayout_align = QtWidgets.QFormLayout()
        self.formLayout_align.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_align.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_align.setSpacing(0)
        self.formLayout_align.setObjectName("formLayout_align")
        self.alignLabel = QtWidgets.QLabel(self.groupBox_3)
        self.alignLabel.setObjectName("alignLabel")
        self.formLayout_align.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.alignLabel)
        self.alignCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.alignCheckBox.setObjectName("alignCheckBox")
        self.formLayout_align.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.alignCheckBox)
        self.horizontalLayout_3.addLayout(self.formLayout_align)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.horizontalLayoutParameters = QtWidgets.QHBoxLayout()
        self.horizontalLayoutParameters.setObjectName("horizontalLayoutParameters")
        self.groupBoxSignalA = QtWidgets.QGroupBox(WidgetSplit)
        self.groupBoxSignalA.setObjectName("groupBoxSignalA")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBoxSignalA)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayoutSignalA = QtWidgets.QFormLayout()
        self.formLayoutSignalA.setObjectName("formLayoutSignalA")
        self.originXLabelSignalA = QtWidgets.QLabel(self.groupBoxSignalA)
        self.originXLabelSignalA.setObjectName("originXLabelSignalA")
        self.formLayoutSignalA.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.originXLabelSignalA)
        self.originXSpinBoxSignalA = QtWidgets.QSpinBox(self.groupBoxSignalA)
        self.originXSpinBoxSignalA.setMaximum(99999)
        self.originXSpinBoxSignalA.setObjectName("originXSpinBoxSignalA")
        self.formLayoutSignalA.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.originXSpinBoxSignalA)
        self.originYLabelSignalA = QtWidgets.QLabel(self.groupBoxSignalA)
        self.originYLabelSignalA.setObjectName("originYLabelSignalA")
        self.formLayoutSignalA.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.originYLabelSignalA)
        self.originYSpinBoxSignalA = QtWidgets.QSpinBox(self.groupBoxSignalA)
        self.originYSpinBoxSignalA.setMaximum(99999)
        self.originYSpinBoxSignalA.setObjectName("originYSpinBoxSignalA")
        self.formLayoutSignalA.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.originYSpinBoxSignalA)
        self.widthLabelSignalA = QtWidgets.QLabel(self.groupBoxSignalA)
        self.widthLabelSignalA.setObjectName("widthLabelSignalA")
        self.formLayoutSignalA.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.widthLabelSignalA)
        self.widthSpinBoxSignalA = QtWidgets.QSpinBox(self.groupBoxSignalA)
        self.widthSpinBoxSignalA.setMaximum(99999)
        self.widthSpinBoxSignalA.setObjectName("widthSpinBoxSignalA")
        self.formLayoutSignalA.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.widthSpinBoxSignalA)
        self.heightLabelSignalA = QtWidgets.QLabel(self.groupBoxSignalA)
        self.heightLabelSignalA.setObjectName("heightLabelSignalA")
        self.formLayoutSignalA.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.heightLabelSignalA)
        self.heightSpinBoxSignalA = QtWidgets.QSpinBox(self.groupBoxSignalA)
        self.heightSpinBoxSignalA.setMaximum(99999)
        self.heightSpinBoxSignalA.setObjectName("heightSpinBoxSignalA")
        self.formLayoutSignalA.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.heightSpinBoxSignalA)
        self.verticalLayout.addLayout(self.formLayoutSignalA)
        self.horizontalLayoutParameters.addWidget(self.groupBoxSignalA)
        self.groupBoxSignalB = QtWidgets.QGroupBox(WidgetSplit)
        self.groupBoxSignalB.setObjectName("groupBoxSignalB")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBoxSignalB)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayoutSignalB = QtWidgets.QFormLayout()
        self.formLayoutSignalB.setObjectName("formLayoutSignalB")
        self.originYLabelSignalB = QtWidgets.QLabel(self.groupBoxSignalB)
        self.originYLabelSignalB.setObjectName("originYLabelSignalB")
        self.formLayoutSignalB.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.originYLabelSignalB)
        self.originYSpinBoxSignalB = QtWidgets.QSpinBox(self.groupBoxSignalB)
        self.originYSpinBoxSignalB.setMaximum(99999)
        self.originYSpinBoxSignalB.setObjectName("originYSpinBoxSignalB")
        self.formLayoutSignalB.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.originYSpinBoxSignalB)
        self.widthLabelSignalB = QtWidgets.QLabel(self.groupBoxSignalB)
        self.widthLabelSignalB.setObjectName("widthLabelSignalB")
        self.formLayoutSignalB.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.widthLabelSignalB)
        self.widthSpinBoxSignalB = QtWidgets.QSpinBox(self.groupBoxSignalB)
        self.widthSpinBoxSignalB.setMaximum(99999)
        self.widthSpinBoxSignalB.setObjectName("widthSpinBoxSignalB")
        self.formLayoutSignalB.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.widthSpinBoxSignalB)
        self.heightLabelSignalB = QtWidgets.QLabel(self.groupBoxSignalB)
        self.heightLabelSignalB.setObjectName("heightLabelSignalB")
        self.formLayoutSignalB.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.heightLabelSignalB)
        self.heightSpinBoxSignalB = QtWidgets.QSpinBox(self.groupBoxSignalB)
        self.heightSpinBoxSignalB.setMaximum(99999)
        self.heightSpinBoxSignalB.setObjectName("heightSpinBoxSignalB")
        self.formLayoutSignalB.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.heightSpinBoxSignalB)
        self.originXLabelSignalB = QtWidgets.QLabel(self.groupBoxSignalB)
        self.originXLabelSignalB.setObjectName("originXLabelSignalB")
        self.formLayoutSignalB.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.originXLabelSignalB)
        self.originXSpinBoxSignalB = QtWidgets.QSpinBox(self.groupBoxSignalB)
        self.originXSpinBoxSignalB.setMaximum(99999)
        self.originXSpinBoxSignalB.setObjectName("originXSpinBoxSignalB")
        self.formLayoutSignalB.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.originXSpinBoxSignalB)
        self.verticalLayout_2.addLayout(self.formLayoutSignalB)
        self.horizontalLayoutParameters.addWidget(self.groupBoxSignalB)
        self.verticalLayout_3.addLayout(self.horizontalLayoutParameters)
        self.buttonBox = QtWidgets.QDialogButtonBox(WidgetSplit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(WidgetSplit)
        QtCore.QMetaObject.connectSlotsByName(WidgetSplit)

    def retranslateUi(self, WidgetSplit):
        _translate = QtCore.QCoreApplication.translate
        WidgetSplit.setWindowTitle(_translate("WidgetSplit", "Split Video"))
        self.groupBox_3.setTitle(_translate("WidgetSplit", "Options"))
        self.lockDimensionsLabel.setText(_translate("WidgetSplit", "Lock Dimensions"))
        self.alignLabel.setText(_translate("WidgetSplit", "Align"))
        self.groupBoxSignalA.setTitle(_translate("WidgetSplit", "Signal A"))
        self.originXLabelSignalA.setText(_translate("WidgetSplit", "Origin X"))
        self.originYLabelSignalA.setText(_translate("WidgetSplit", "Origin Y"))
        self.widthLabelSignalA.setText(_translate("WidgetSplit", "Width"))
        self.heightLabelSignalA.setText(_translate("WidgetSplit", "Height"))
        self.groupBoxSignalB.setTitle(_translate("WidgetSplit", "Signal B (NEW)"))
        self.originYLabelSignalB.setText(_translate("WidgetSplit", "Origin Y"))
        self.widthLabelSignalB.setText(_translate("WidgetSplit", "Width"))
        self.heightLabelSignalB.setText(_translate("WidgetSplit", "Height"))
        self.originXLabelSignalB.setText(_translate("WidgetSplit", "Origin X"))

