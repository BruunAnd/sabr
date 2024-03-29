package com.sabr.communication;

import com.sabr.abortion.IAbortable;

public class ConnectionFactory
{
    public Connection createInstance(ConnectionType type, IAbortable abortable)
    {
        switch (type)
        {
            case Bluetooth:
                return new BluetoothConnection(abortable);
            default:
                throw new UnsupportedOperationException();
        }
    }

    public enum ConnectionType
    {
        Bluetooth
    }
}
