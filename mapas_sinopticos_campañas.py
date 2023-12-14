


fig = plt.figure(figsize=(8, 8))
ax1 = plt.subplot(projection=ccrs.Mercator())
ax2 = plt.subplot(projection=ccrs.Mercator())
ax1.set_extent([lon_w, lon_e, lat_s, lat_n], crs=ccrs.PlateCarree())
ax1.coastlines(resolution='50m', color='black', linewidths=0.4, zorder=5)
gl = ax1.gridlines(crs=ccrs.PlateCarree(central_longitude=0), draw_labels=True,
                   linewidth=.5, color='gray', alpha=0.5, linestyle='--', zorder=6)
gl.xlabels_top = gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
cl = ax2.contourf(lons, lats, var, clevs, cmap=cmap, alpha=0.9, transform=ccrs.PlateCarree(), extend='both')
# cline = plt.contour(lons, lats, var,[4.8,5.6], colors='k', linewidths=.5, transform=ccrs.PlateCarree(),
#                    zorder=7)
# plt.clabel(cline, inline=1, inline_spacing=-3, fmt='%2.1f', fontsize=7, colors='k')
cb = fig.colorbar(cl, aspect=40, orientation='horizontal', pad=0.09)
cb.ax.set_title(nombre_var, fontsize=10)
ax1.set_title(title)
fig.savefig(nombre_salida + '.png', dpi=300, bbox_inches='tight')