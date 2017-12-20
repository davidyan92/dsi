import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from ipywidgets import *

from pprint import pprint

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (roc_curve, auc, f1_score,
                             precision_recall_curve, average_precision_score)


class ROCLogisticPlotter(object):

    def __init__(self, separations=range(0,101),
                 proportions=range(5,96,5)):

        self.cancer = np.random.random(size=200)*10.
        self.healthy = np.random.random(size=200)*10.

        self.cr = (np.random.random(size=200)*0.3)+0.7
        self.hr = (np.random.random(size=200)*0.3)+0.7

        self.separations = separations
        self.proportions = proportions

        self.colors = {'blue': '#729ECE',
                       'brown': '#A8786E',
                       'green': '#67BF5C',
                       'grey': '#A2A2A2',
                       'orange': '#FF9E4A',
                       'pink': '#ED97CA',
                       'purple': '#AD8BC9',
                       'red': '#ED665D',
                       'teal': '#6DCCDA',
                       'yellow': '#CDCC5D'}

        self.dark_colors = dict(blue='#1F77B4',
                                orange='#FF7F0E',
                                green='#2CA02C',
                                red='#D62728',
                                purple='#9467BD',
                                brown='#8C564B',
                                pink='#E377C2',
                                grey='#7F7F7F',
                                yellow='#BCBD22',
                                teal='#17BECF')


    def separator(self, x, r, separation=0.01, increase=True):

        if increase:
            diffs = 10.-x
        else:
            diffs = x

        diffs = r * (diffs * separation)

        if increase:
            return x + diffs
        else:
            return x - diffs


    def find_max_sep(self, cancer_seps, healthy_seps):

        max_sep = 0
        for s in self.separations:
            min_cancer = np.min(cancer_seps[s])
            max_healthy = np.max(healthy_seps[s])

            if max_healthy < min_cancer:
                max_sep = s

        return max_sep


    def construct_seps(self, cancer, healthy):
        cancer_seps = {}
        healthy_seps = {}

        for s in self.separations:
            s_ = s/100.
            cancer_seps[s] = self.separator(cancer, self.cr[:len(cancer)], separation=s_)
            healthy_seps[s] = self.separator(healthy, self.hr[:len(healthy)],
                                             separation=s_, increase=False)

        return cancer_seps, healthy_seps


    def fit_logregs(self, cancer_seps, healthy_seps):

        lrs = {}
        fprs = {}
        tprs = {}
        aucs = {}
        accs = {}
        precisions = {}
        recalls = {}
        avg_precisions = {}
        f1s = {}
        y_preds = {}
        y_pps = {}
        y_trues = {}

        for s in self.separations:

            cancer = cancer_seps[s]
            healthy = healthy_seps[s]

            y = np.concatenate([np.ones(len(cancer)), np.zeros(len(healthy))])
            X = np.concatenate([cancer, healthy])[:,np.newaxis]

            lr = LogisticRegression()
            lr.fit(X, y)
            y_pp = lr.predict_proba(X)[:, 1]
            y_pred = lr.predict(X)

            fpr_, tpr_, _ = roc_curve(y, y_pp)
            auc_ = auc(fpr_, tpr_)
            acc_ = np.abs(0.5 - np.mean(y)) + 0.5

            precision, recall, _ = precision_recall_curve(y, y_pp)
            avg_precision = average_precision_score(y, y_pp)
            f1 = f1_score(y, y_pred)

            lrs[s] = lr
            fprs[s] = fpr_
            tprs[s] = tpr_
            aucs[s] = auc_
            accs[s] = acc_
            precisions[s] = precision
            recalls[s] = recall
            avg_precisions[s] = avg_precision
            f1s[s] = f1
            y_preds[s] = y_pred
            y_pps[s] = y_pp
            y_trues[s] = y

        return (lrs, fprs, tprs, aucs, accs, precisions,
                recalls, avg_precisions, f1s, y_preds, y_pps, y_trues)


    def preconstruct_data(self):
        self.class_balances = {}

        print 'Constructing data'
        for p in self.proportions:
            cancer = self.cancer[:p]
            healthy = self.healthy[:(100-p)]

            cseps, hseps = self.construct_seps(cancer, healthy)
            max_sep = self.find_max_sep(cseps, hseps)

            lrs, fprs, tprs, aucs, accs, precisions, recalls, \
            avg_precisions, f1s, y_preds, y_pps, y_trues = self.fit_logregs(cseps, hseps)

            self.class_balances[p] = {
                'cancer':cseps,
                'healthy':hseps,
                'max_sep':max_sep,
                'logregs':lrs,
                'fprs':fprs,
                'tprs':tprs,
                'aucs':aucs,
                'accs':accs,
                'precisions':precisions,
                'recalls':recalls,
                'avg_precisions':avg_precisions,
                'f1s':f1s,
                'y_preds':y_preds,
                'y_pps':y_pps,
                'y_trues':y_trues
            }


    def plot_roc_aupr(self, proportion, separation, threshold, prauc=False):

        cancer = self.class_balances[proportion]['cancer'][separation]
        healthy = self.class_balances[proportion]['healthy'][separation]
        mod = self.class_balances[proportion]['logregs'][separation]
        fpr_ = self.class_balances[proportion]['fprs'][separation]
        tpr_ = self.class_balances[proportion]['tprs'][separation]
        auc_ = self.class_balances[proportion]['aucs'][separation]
        acc_ = self.class_balances[proportion]['accs'][separation]
        pre_ = self.class_balances[proportion]['precisions'][separation]
        rec_ = self.class_balances[proportion]['recalls'][separation]
        avgp_ = self.class_balances[proportion]['avg_precisions'][separation]
        f1_ = self.class_balances[proportion]['f1s'][separation]
        y_pred = self.class_balances[proportion]['y_preds'][separation]
        y_pp = self.class_balances[proportion]['y_pps'][separation]
        y_true = self.class_balances[proportion]['y_trues'][separation]

        self.currents = {
            'cancer':cancer,
            'healthy':healthy,
            'model':mod,
            'fpr':fpr_,
            'tpr':tpr_,
            'auc':auc_,
            'accuracy':acc_,
            'precision':pre_,
            'recall':rec_,
            'avg_precision':avgp_,
            'f1_score':f1_,
            'y_pred':y_pred,
            'y_pp':y_pp,
            'y_true':y_true
        }

        fig, axarr = plt.subplots(1, 2, figsize=(18,7.5))

        ax = axarr[1]
        axr = axarr[0]

        # plot the logreg regression line for admit ~ gpa
        x_vals = np.linspace(-1.,12.,300)
        y_pp = mod.predict_proba(x_vals[:, np.newaxis])[:,1]

        pp_r = [np.floor(pp*100.) for pp in y_pp]
        pp_xs = {}
        for x_, p_ in zip(x_vals, pp_r):
            if p_ not in pp_xs.keys():
                pp_xs[p_] = x_

        sortedkeys = sorted(pp_xs.keys())
        if threshold < np.min(sortedkeys):
            threshold = np.min(sortedkeys)
        if threshold > np.max(sortedkeys):
            threshold = np.max(sortedkeys)

        ax.plot(x_vals, y_pp, color='black', alpha=0.6, lw=4)

        # do one scatter plot for each type of wine:
        ax.scatter(cancer,
                   np.ones(len(cancer)),
                   c=self.dark_colors['orange'], s=100, alpha=0.7,
                   label='cancer')

        ax.scatter(healthy,
                   np.zeros(len(healthy)),
                   c=self.dark_colors['blue'], s=100, alpha=0.7,
                   label='healthy')

        ax.vlines(pp_xs[threshold], ymin=-0.2, ymax=1.2,
                   lw=3, color=self.dark_colors['red'],
                   linestyles='dashed')

        ax.hlines(threshold/100., xmin=-5, xmax=pp_xs[threshold],
                   lw=3, color=self.dark_colors['red'],
                   linestyles='dashed',
                   label='diagnosis threshold')

        ax.fill_between(x_vals[x_vals >= pp_xs[threshold]], 0, 1,
                               facecolor=self.dark_colors['orange'], alpha=0.15)
        ax.fill_between(x_vals[x_vals < pp_xs[threshold]], 0, 1,
                               facecolor=self.dark_colors['blue'], alpha=0.15)

        ax.set_ylabel('cancer vs. healthy', fontsize=16)
        ax.set_xlabel('tumor size', fontsize=16)
        ax.set_title('cancer probability by tumor size\n', fontsize=20)

        ax.set_xlim([-0.5, 10.5])
        ax.set_ylim([-0.1, 1.1])

        ax.legend(loc='lower right', fontsize=12)

        tps = (cancer > pp_xs[threshold])
        fps = (healthy > pp_xs[threshold])
        tns = (healthy < pp_xs[threshold])
        fns = (cancer < pp_xs[threshold])


        ax.annotate('TP='+str(sum(tps)), xy=(0.85, 0.7), xycoords='axes fraction',
                    xytext=(0.85, 0.7), textcoords='axes fraction',
                    horizontalalignment='center', verticalalignment='center',
                    fontsize=18, fontweight='bold')

        ax.annotate('FP='+str(sum(fps)), xy=(0.85, 0.3), xycoords='axes fraction',
                    xytext=(0.85, 0.3), textcoords='axes fraction',
                    horizontalalignment='center', verticalalignment='center',
                    fontsize=18, fontweight='bold')

        ax.annotate('TN='+str(sum(tns)), xy=(0.15, 0.3), xycoords='axes fraction',
                    xytext=(0.15, 0.3), textcoords='axes fraction',
                    horizontalalignment='center', verticalalignment='center',
                    fontsize=18, fontweight='bold')

        ax.annotate('FN='+str(sum(fns)), xy=(0.15, 0.7), xycoords='axes fraction',
                    xytext=(0.15, 0.7), textcoords='axes fraction',
                    horizontalalignment='center', verticalalignment='center',
                    fontsize=18, fontweight='bold')

        if not prauc:

            tpr_crit = np.sum(tps)/float(len(cancer))
            fpr_crit = np.sum(fps)/float(len(healthy))

            # Plot of a ROC curve for class 1 (has_cancer)
            axr.plot(fpr_, tpr_, label='ROC (area = %0.2f)' % auc_,
                     color=self.dark_colors['purple'], linewidth=4,
                     alpha=0.7)
            axr.plot([0, 1], [0, 1], color=self.dark_colors['grey'], ls='dashed',
                     alpha=0.9, linewidth=4, label='baseline accuracy = %0.2f' % acc_)

            axr.vlines(fpr_crit, ymin=-0.3, ymax=tpr_crit,
                       lw=3, color=self.dark_colors['red'], linestyles='dashed')
            axr.hlines(tpr_crit, xmin=-0.3, xmax=fpr_crit,
                       lw=3, color=self.dark_colors['red'], linestyles='dashed')

            axr.set_xlim([-0.05, 1.05])
            axr.set_ylim([0.0, 1.05])
            axr.set_xlabel('false positive rate', fontsize=16)
            axr.set_ylabel('true positive rate', fontsize=16)
            axr.set_title('cancer vs. healthy ROC curve\n', fontsize=20)


            axr.legend(loc="lower right", fontsize=16)

        else:

            axr.plot(rec_, pre_, label='Avg. precision (area = %0.2f)' % avgp_,
                     color=self.dark_colors['purple'], linewidth=4,
                     alpha=0.7)

            rec_line = np.sum(tps)/float((np.sum(tps) + np.sum(fns)))
            pre_line = np.sum(tps)/float((np.sum(tps) + np.sum(fps)))

            axr.vlines(rec_line, ymin=-0.3, ymax=pre_line,
                       lw=3, color=self.dark_colors['red'], linestyles='dashed')
            axr.hlines(pre_line, xmin=-0.3, xmax=rec_line,
                       lw=3, color=self.dark_colors['red'], linestyles='dashed')

            axr.set_xlim([-0.05, 1.05])
            axr.set_ylim([0.0, 1.05])
            axr.set_xlabel('recall, TP/(TP+FN)', fontsize=16)
            axr.set_ylabel('precision, TP/(TP+FP)', fontsize=16)
            axr.set_title('cancer vs. healthy PR curve\n', fontsize=20)

            axr.annotate('F1-score = %0.2f' % f1_, xy=(0.85, 0.85),
                         xycoords='axes fraction',
                         xytext=(0.85, 0.85), textcoords='axes fraction',
                         horizontalalignment='center', verticalalignment='center',
                         fontsize=18, fontweight='bold')

            axr.legend(loc="upper right", fontsize=16)

        plt.show()


    def roc_logreg_wrapper(self, dispersion=50, diagnosis_criterion=0.5,
                           cancer_proportion=0.5, pr_curve=False):
        self.plot_roc_aupr(int(cancer_proportion*100),
                           100-dispersion, int(diagnosis_criterion*100),
                           prauc=pr_curve)


    def roc_interact(self):


        cp = widgets.FloatSlider(min=.05, max=.95, step=.05, value=.50)
        cp.width = '600px'

        disp = widgets.IntSlider(min=np.min(self.separations),
                                 max=np.max(self.separations),
                                 step=1, value=75)
        disp.width = '600px'

        thresh = widgets.FloatSlider(min=.01, max=.99, step=.01, value=.50)
        thresh.width = '600px'

        pr = widgets.Checkbox(value=False)
        pr.description = 'PR curve:'

        cp.description = 'cancer %:'
        disp.description = 'spread:'
        thresh.description = 'threshold:'


        widgets.interact(self.roc_logreg_wrapper,
                         cancer_proportion=cp,
                         dispersion=disp,
                         diagnosis_criterion=thresh,
                         pr_curve=pr)
