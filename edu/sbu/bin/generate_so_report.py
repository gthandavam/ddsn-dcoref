__author__ = 'gt'
import csv

dishes = (
'BananaMuffins',
'BeefChilli',
'BeefMeatLoaf',
'BeefStroganoff',
'CarrotCake',
'CheeseBurger',
'ChickenSalad',
'ChickenStirFry',
'Coleslaw',
'CornChowder',
'DeviledEggs',
'EggNoodles',
'FrenchToast',
'MacAndCheese',
'MeatLasagna',
'PecanPie',
'PotatoSalad',
'PulledPork',
'PumpkinPie',
'VeggiePizza'
)


experiments = (
  'UGBG_CP__prob_wt_arbor_trans',
# 'UGBG_CP_01234_indicator_arbor',
# 'UGBG_CP_01234_indicator_arbor_trans',
# 'UGBG_CP_01234_indicator_cc',
# 'UGBG_CP_01234_indicator_text_order',
# 'UG_CP_01234_indicator_arbor',
# 'UG_CP_01234_indicator_arbor_trans',
# 'UG_CP_01234_indicator_cc',
# 'UG_CP_01234_indicator_text_order',
# 'UGBG_CP_01234_prob_wt_arbor',
# 'UGBG_CP_01234_prob_wt_arbor_trans',
# 'UGBG_CP_01234_prob_wt_cc',
# 'UGBG_CP_01234_prob_wt_text_order',
# 'UG_CP_01234_prob_wt_arbor',
# 'UG_CP_01234_prob_wt_arbor_trans',
# 'UG_CP_01234_prob_wt_cc',
# 'UG_CP_01234_prob_wt_text_order'

)



def main():
  docRoot = '/home/gt/Documents/'
  with open('/home/gt/Documents/so_report_with_obj_func.csv', 'w') as report:
    writer = csv.writer(report)

    for dish in dishes:
      writer.writerow([dish])
      writer.writerow(['Features', 'TPR', 'FPR', 'Observed +', 'Observed -', 'SVM Classification Acc.', 'kTau average (TSP with SVM Prob)', 'global inference - Class. Acc. (TSP with SVM Prob)', 'kTau average (TSP with CP{1,2,3,4})', 'global inference - Class. Acc. (TSP with CP{1,2,3,4})'])
      for experiment in experiments:
        fileName = docRoot + dish + '/log/' + dish + '_' + experiment + '.out'
        # row = [experiment]
        row = ['UG BG C Tuned with 5 fold Cross Validation']
        with open(fileName) as logF:
          #special flag since pred_accuracy is in a separate line in logFile
          pred_accuracy_line = False
          for line in logF.readlines():
            if(pred_accuracy_line):
              row.append(line.strip())
              pred_accuracy_line = False
              continue
            if line.startswith('TPR') or line.startswith('FPR') :
              row.append(line.split(' ')[1].strip())
            elif line.startswith('Observed +') or line.startswith('Observed -'):
              row.append(line.split(' ')[2].strip())
            elif line.startswith('prediction accuracy...') :
              pred_accuracy_line = True
            elif line.startswith('Average'):
              row.append(line.split(':')[1].strip())
            elif line.startswith('global'):
              row.append(line.split('...')[1].strip())
              pass
            pass

        writer.writerow(row)
      pass

  pass


if __name__ == '__main__':
  main()