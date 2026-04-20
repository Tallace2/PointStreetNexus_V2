@echo off
echo --- Point Street Nexus: Opening SQL Server Ports ---
echo.

echo Opening TCP Port 1433 (Default SQL)...
netsh advfirewall firewall add rule name="SQL Server (1433)" dir=in action=allow protocol=TCP localport=1433

echo Opening UDP Port 1434 (SQL Browser)...
netsh advfirewall firewall add rule name="SQL Browser (1434)" dir=in action=allow protocol=UDP localport=1434

echo.
echo SUCCESS: Firewall rules added.
echo PLEASE ENSURE 'SQL SERVER BROWSER' SERVICE IS RUNNING IN COMPUTER MANAGEMENT.
pause
