# plot channel utilization for CONETSI

import pandas as pd
import matplotlib.pyplot as plt
import plotting as pt
import numpy as np

H = 40      # number of bytes of headers

data = pd.read_csv("../logs-conetsi/utilization3.log").values[:, 1:]
print data

txed = dict()   # bytes txed per node
txedindiv = dict()   # bytes txed per node if sent without conetsi
sizes = dict()
hops = dict()
for row in data:
    if sizes.has_key(row[-1]):
        sizes[row[-1]].append(row[1])
        hops[row[-1]].append(row[-2])
    else:
        sizes[row[-1]] = [row[1]]
        hops[row[-1]] = [row[-2]]

    if txed.has_key(row[-2]):
        txed[row[-2]].append((row[1]+H) * row[-2]/(1.0 * row[0]))
        txedindiv[row[-2]].append((row[1] + H * row[0]) * row[-2] / (1.0 * row[0]))
    else:
        txed[row[-2]] = [(row[1]+H) * row[-2]/(1.0 * row[0])]
        txedindiv[row[-2]] = [(row[1] + H * row[0]) * row[-2]/(1.0 * row[0])]

#print sizes.values()
#print hops.values()
a = [np.mean(x) for x in txed.values()]
b = [np.mean(x) for x in txedindiv.values()]

print a, b

for (aa, bb) in zip(a, b):
    print (bb - aa) * 100.0 / aa

fig, ax = pt.plot_violin(sizes.values(),
                    xlabel=r"\textbf{Number of neighbours}",
                    ylabel=r"\textbf{Size of NSI}",
                    leg=True, x_tick_labels=[1,2,3,4,5,6,7,8,9,10,11])

fig2 = plt.figure(figsize=(10,8))
ax2 = fig2.add_subplot(111)
#plt.subplots_adjust(bottom=0.22, right=0.97, top=0.97, left=0.15)

fs_norm = 11

tmp = [np.mean(x) for x in txed.values()]
ax2.plot([1,2,3], tmp[:-1], color='b', lw=0.8, lineStyle='-', marker='o', markersize=2.5, alpha=0.7)
#fig3, ax3 = pt.plot_violin(txed.values(),
#                    xlabel="Hops to genesis node ($g$)",
#                    ylabel="Transmitted bytes",
#                    leg=True)
tmp2 = [np.mean(x) for x in txedindiv.values()]
ax2.plot([1,2,3], tmp2[:-1], color='r', lw=0.8, lineStyle='-', marker='o', markersize=2.5, alpha=0.7)
ax2.set_xlabel(r"\textbf{Hops to genesis node ($g$)}", fontsize=fs_norm-2)
ax2.set_ylabel(r"\textbf{Transmitted bytes}", fontsize=fs_norm-2)

ax2.legend(labels=['CONETSI', 'Trivial'],
           shadow=False, fontsize=fs_norm-4, ncol=1,
           loc=(0.01, 0.75), framealpha=0.65)

ax2.set_xticks([1, 2, 3])
#ax.set_xticklabels([1,2,3], rotation='0')
#plt.tick_params(labelsize=fs_norm-3)

#plt.grid();
# IEEE format width this 88mm per column
# set size to 8.9 cm 
fig.set_size_inches(w=8.8/2.54, h=4.7/(2.54 * 0.98))
fig.savefig('sizevsneigh.pdf', format='pdf')

#fig2.set_size_inches(w=8.8/2.54, h=4.7/(2.54 * 0.98))
#fig2.savefig('bytesvshop.pdf', format='pdf')

#fig2, ax2 = pt.plot_violin(hops.values())
#plt.show()
