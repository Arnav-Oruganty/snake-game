import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, rolling_avg):
    plt.clf()
    plt.plot(scores, label='Score', color='cornflowerblue', alpha=0.7, linewidth=1.5, linestyle='-')
    plt.plot(rolling_avg, label='Rolling_avg', color='orange', alpha=0.7, linewidth=2, linestyle='-')
    plt.text(len(scores) - 1, scores[-1], f'{scores[-1]}', ha='center', va='bottom', fontsize=10, color='blue',
             weight='bold')
    plt.text(len(rolling_avg) - 1, rolling_avg[-1], f'{rolling_avg[-1]:.2f}', ha='center', va='bottom', fontsize=10,
             color='orange', weight='bold')
    plt.legend(loc='upper left', shadow=True, fontsize='medium')
    plt.tick_params(axis='both', which='major', labelsize=8)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.title('Training Progress', fontsize=14)
    plt.xlabel('Number of Games', fontsize=10)
    plt.ylabel('Score', fontsize=10)
    plt.ylim(0, max(max(scores), max(rolling_avg)) * 1.1)
    plt.tight_layout()
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.show(block=False)
    plt.pause(.1)