"""
Módulo de anonimización de datasets
Funciones reutilizables para hashear IDs y eliminar PII
"""

import hashlib
import pandas as pd
from typing import Optional

class DataAnonymizer:
    """Clase para anonimizar datasets de forma consistente"""
    
    def __init__(self, salt: str):
        """
        Inicializar con un salt criptográfico
        
        Args:
            salt (str): String secreto para hashing (debe guardarse en .env)
        """
        self.salt = salt
    
    def hash_id(self, value: str, hash_length: int = 12) -> str:
        """
        Hashear un ID con SHA-256 + salt
        
        Args:
            value (str): Valor a hashear
            hash_length (int): Largo del hash resultante (default 12)
        
        Returns:
            str: Hash hexadecimal
        
        Example:
            >>> anon = DataAnonymizer("mi_salt_secreto")
            >>> anon.hash_id("ALS0001")
            '19e503ba5c1c'
        """
        return hashlib.sha256(f"{value}{self.salt}".encode()).hexdigest()[:hash_length]
    
    def anonymize_column(self, series: pd.Series, hash_length: int = 12) -> pd.Series:
        """
        Hashear una columna completa de pandas Series
        
        Args:
            series (pd.Series): Columna a hashear
            hash_length (int): Largo del hash (default 12)
        
        Returns:
            pd.Series: Columna hasheada
        """
        return series.apply(lambda x: self.hash_id(x, hash_length))
    
    def drop_columns(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """
        Eliminar columnas PII críticas
        
        Args:
            df (pd.DataFrame): DataFrame
            columns (list): Lista de columnas a eliminar
        
        Returns:
            pd.DataFrame: DataFrame sin esas columnas
        """
        return df.drop(columns=columns, errors='ignore')
    
    def convert_to_datetime(self, df: pd.DataFrame, columns: dict) -> pd.DataFrame:
        """
        Convertir columnas a datetime
        
        Args:
            df (pd.DataFrame): DataFrame
            columns (dict): {nombre_columna: formato_datetime}
        
        Returns:
            pd.DataFrame: DataFrame con columnas convertidas
        
        Example:
            >>> df = anon.convert_to_datetime(df, {'FechaProceso': '%d/%m/%Y'})
        """
        for col, fmt in columns.items():
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], format=fmt)
        return df
    
    def anonymize_dataset(self, 
                         df: pd.DataFrame,
                         drop_cols: Optional[list] = None,
                         hash_cols: Optional[dict] = None,
                         datetime_cols: Optional[dict] = None) -> pd.DataFrame:
        """
        Pipeline completo de anonimización
        
        Args:
            df (pd.DataFrame): Dataset a anonimizar
            drop_cols (list): Columnas a eliminar
            hash_cols (dict): {columna: hash_length}
            datetime_cols (dict): {columna: formato}
        
        Returns:
            pd.DataFrame: Dataset anonimizado
        
        Example:
            >>> anon = DataAnonymizer("mi_salt")
            >>> df_clean = anon.anonymize_dataset(
            ...     df,
            ...     drop_cols=['NombreCliente2'],
            ...     hash_cols={'IdCliente': 12},
            ...     datetime_cols={'FechaProceso': '%d/%m/%Y'}
            ... )
        """
        # Paso 1: Eliminar columnas críticas
        if drop_cols:
            df = self.drop_columns(df, drop_cols)
            print(f"✓ Eliminadas columnas: {drop_cols}")
        
        # Paso 2: Hashear IDs
        if hash_cols:
            for col, length in hash_cols.items():
                if col in df.columns:
                    df[col] = self.anonymize_column(df[col], length)
                    print(f"✓ Hasheada columna: {col}")
        
        # Paso 3: Convertir fechas
        if datetime_cols:
            df = self.convert_to_datetime(df, datetime_cols)
            print(f"✓ Convertidas a datetime: {list(datetime_cols.keys())}")
        
        return df