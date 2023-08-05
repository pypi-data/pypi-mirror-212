from similari import (
    Sort,
    Universal2DBox,
    SpatioTemporalConstraints,
    PositionalMetricType,
)

BOXES_1 = [
    [654.375, 418.359375, -1.08950759090885, 0.06182759814798534, 340.5220642089844],
    [550.3125, 379.3359375, -1.129803881362839, 0.07216824447658342, 293.8331604003906],
    [
        125.15625,
        355.60546875,
        -0.6551687205652192,
        0.1363352988349452,
        182.83360290527344,
    ],
    [839.375, 329.4140625, 0.9311933167479997, 0.07460492907503219, 287.0589904785156],
    [555.0, 551.6015625, -0.5173672116741088, 0.06403988519157659, 366.5615234375],
    [380.9375, 265.078125, -1.2747445594776385, 0.05473158703331464, 354.41259765625],
    [
        242.1875,
        308.14453125,
        -0.2078592736722506,
        0.06851543739648944,
        304.702392578125,
    ],
    [927.5, 485.859375, -0.02181425001386707, 0.059192059468350856, 310.4801940917969],
    [725.625, 556.875, -0.23166345637797628, 0.08713287963547522, 184.94488525390625],
    [
        864.375,
        502.3828125,
        0.24739611380713303,
        0.05943324441452824,
        316.27691650390625,
    ],
    [668.75, 381.4453125, -0.8396859698494138, 0.07229550543674212, 305.55511474609375],
    [288.4375, 433.125, -0.17867848497603436, 0.06008579970810128, 336.22802734375],
    [662.5, 232.55859375, -0.5881607246406537, 0.0673030215962557, 297.13165283203125],
    [
        229.21875,
        409.21875,
        -0.1168992563119464,
        0.05855327449025996,
        353.38519287109375,
    ],
    [
        316.09375,
        103.53515625,
        -1.2623163856185657,
        0.06354494174959537,
        285.65826416015625,
    ],
    [
        514.375,
        114.873046875,
        0.844491710615489,
        0.07671649949878948,
        260.29510498046875,
    ],
    [
        126.09375,
        605.0390625,
        -0.29419124969021504,
        0.11571208548527089,
        215.46337890625,
    ],
    [
        413.75,
        213.92578125,
        -0.9657712011303433,
        0.07631818226761462,
        293.21502685546875,
    ],
    [451.25, 447.890625, -0.6795026892355458, 0.07388564032534921, 314.9710693359375],
    [818.75, 131.30859375, -1.3748421322093567, 0.06306835024561531, 266.639404296875],
    [856.25, 227.109375, -1.566501180588817, 0.059453860794436535, 274.05706787109375],
    [917.5, 101.42578125, -1.2209488386160925, 0.0685205241197251, 276.1524353027344],
    [727.5, 172.001953125, -1.3254025439428534, 0.08630334951440506, 187.4688720703125],
]

BOXES_2 = [
    [534.375, 368.4375, -1.101980439295209, 0.07122194536958791, 294.6826171875],
    [655.625, 418.359375, -1.09799175635157, 0.060449629503938826, 340.4578857421875],
    [864.375, 501.328125, 0.2527380654139389, 0.056794797327308334, 326.08819580078125],
    [
        242.1875,
        301.9921875,
        -0.22382585651365716,
        0.06272859667119125,
        319.5481262207031,
    ],
    [376.5625, 261.2109375, -1.283783461375422, 0.05985874299287419, 338.7218322753906],
    [
        125.15625,
        355.078125,
        -0.6595017502378054,
        0.13481610398035634,
        183.08370971679688,
    ],
    [725.0, 556.875, -0.22640149947241367, 0.08722859430117187, 184.79248046875],
    [
        288.125,
        432.0703125,
        -0.18401136519037714,
        0.06062317187469461,
        334.13873291015625,
    ],
    [928.75, 483.046875, 0.010908012380531129, 0.05898330096331063, 310.26654052734375],
    [668.75, 380.7421875, -0.8257274770489542, 0.07123307222138725, 299.7037353515625],
    [840.0, 328.359375, 0.9279294796740531, 0.07103401647407939, 292.3738098144531],
    [
        316.09375,
        102.3046875,
        -1.2634194669420764,
        0.059841705904805406,
        292.3897399902344,
    ],
    [
        554.6875,
        550.8984375,
        -0.4945779763045692,
        0.06358155933944147,
        365.6000671386719,
    ],
    [662.5, 231.6796875, -0.5988330098140101, 0.06578038672280338, 300.5981750488281],
    [229.21875, 409.21875, -0.1168992563119464, 0.05883235030416289, 350.3829345703125],
    [513.75, 113.90625, 0.8408897186621297, 0.07426706369369915, 264.0218505859375],
    [
        125.546875,
        605.0390625,
        -0.28365944626436046,
        0.11471792490605068,
        216.64146423339844,
    ],
    [
        413.75,
        212.87109375,
        -0.9610671265388818,
        0.07466581785562328,
        294.78729248046875,
    ],
    [451.5625, 447.890625, -0.6795026892355458, 0.07267504740494687, 317.4398193359375],
    [819.375, 129.7265625, -1.369520470561106, 0.0636213571415013, 268.4916076660156],
    [855.625, 225.0, -1.5572955648067945, 0.06000232800760282, 269.3219909667969],
    [918.75, 99.84375, -1.21361023191627, 0.07017798850556049, 272.5237121582031],
    [727.5, 170.595703125, -1.350716023262111, 0.08038329382212916, 191.7749786376953],
]


def create_detections(boxes):
    detections = []
    for box in boxes:
        xc, yc, angle, aspect, height = box
        similari_box = Universal2DBox(
            xc=xc,
            yc=yc,
            angle=angle,
            aspect=aspect,
            height=height,
        )
        detections.append((similari_box, None))

    return detections


def main():
    metric = PositionalMetricType.iou(threshold=0.3)
    # metric = PositionalMetricType.maha()

    tracker = Sort(
        shards=4,
        bbox_history=10,
        max_idle_epochs=5,
        method=metric,
        spatio_temporal_constraints=None,
    )

    tracks = tracker.predict(create_detections(BOXES_1))

    print('predict 1 done')

    tracks = tracker.predict(create_detections(BOXES_2))

    print('predict 2 done')


if __name__ == '__main__':
    main()
