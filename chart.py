import matplotlib.pyplot as plt
from road import Road

def draw_road_charts(roads: list[Road]):
  plt.figure(figsize=(10, 5))

  all_times = []
  all_charges = []

  for road in roads:
    times = [t for _, t in road.cell.chart_data]
    charges = [c for c, _ in road.cell.chart_data]
        
    all_times.extend(times)
    all_charges.extend(charges)

    plt.plot(times, charges, label=road.name)

  plt.title('Battery energy Over Time')
  plt.xlabel('Time (s)')
  plt.ylabel('Energy (J)')
  plt.grid(True)

  if all_times:
    plt.xlim(0, max(all_times) * 1.05)
  if all_charges:
    plt.ylim(0, max(all_charges) * 1.05)

  plt.legend()
  plt.show()