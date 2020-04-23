module LatexTable where

import Data.List (intercalate)

data TableHeader = RowHeader | ColHeader | NoHeader deriving (Eq)
data TableCellEnvironment = DefaultCells | MathCells deriving (Eq)

render :: TableHeader -> TableCellEnvironment -> [String] -> [[String]] -> String
render h env cols rows =
    "\\begin{tabular}{|*{" ++ show (length cols) ++ "}{c|}}\n\\hline\n" ++
    joinRows (fmtCols (headerCell <$> cols) : (fmtCols <$> rows) ++ ["\\end{tabular}"])
    where
        headerCell c
            | h == RowHeader = boldCell c
            | otherwise      = c
        fmtCols (c : cs)
            | h == ColHeader = intercalate " & " (boldCell c : (cell <$> cs))
            | otherwise      = intercalate " & " (cell <$> (c : cs))
        joinRows = intercalate "\\\\\\hline\n"
        boldCell c = "\\textbf{" ++ cell c ++ "}"
        cell c
            | env == MathCells = "$" ++ c ++ "$"
            | otherwise        = c

prependRowHeader :: Monoid a => [a] -> [[a]] -> [[a]]
prependRowHeader (h:hs) (cs:css) = (h:cs) : prependRowHeader hs css
prependRowHeader [] (cs:css) = (mempty:cs) : prependRowHeader [] css
prependRowHeader _ _ = []
