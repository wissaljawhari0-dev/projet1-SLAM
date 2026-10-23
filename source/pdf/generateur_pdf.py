
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable
)


BLEU_FONCE = colors.HexColor("#17365D")
BLEU = colors.HexColor("#2874A6")
BLEU_CLAIR = colors.HexColor("#EAF2F8")
VERT = colors.HexColor("#D5F5E3")
ROUGE = colors.HexColor("#FADBD8")
GRIS = colors.HexColor("#F2F4F4")
GRIS_TEXTE = colors.HexColor("#566573")
BLANC = colors.white


def generer_pdf(nom_profil, resultats, verdict):
    nom_fichier = "PV_Recette.pdf"

    document = SimpleDocTemplate(
        nom_fichier,
        pagesize=A4,
        rightMargin=1.7 * cm,
        leftMargin=1.7 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="TitreProjet",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=28,
        textColor=BLEU_FONCE,
        alignment=TA_CENTER,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name="SousTitre",
        parent=styles["Normal"],
        fontSize=11,
        leading=16,
        textColor=GRIS_TEXTE,
        alignment=TA_CENTER,
        spaceAfter=12
    ))

    styles.add(ParagraphStyle(
        name="TitreSection",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=BLEU_FONCE,
        spaceBefore=12,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name="TexteCellule",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        wordWrap="CJK"
    ))

    styles.add(ParagraphStyle(
        name="CelluleCentre",
        parent=styles["TexteCellule"],
        alignment=TA_CENTER
    ))

    styles.add(ParagraphStyle(
        name="Verdict",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=18,
        alignment=TA_CENTER,
        textColor=BLEU_FONCE
    ))

    elements = []

    # En-tête du rapport
    elements.append(Spacer(1, 0.7 * cm))
    elements.append(Paragraph(
        "PROJET 1 SLAM",
        styles["TitreProjet"]
    ))
    elements.append(Paragraph(
        "RAPPORT DE RECETTE INFORMATIQUE",
        styles["SousTitre"]
    ))
    elements.append(HRFlowable(
        width="100%",
        thickness=2,
        color=BLEU,
        spaceBefore=4,
        spaceAfter=18
    ))

    # Informations générales
    elements.append(Paragraph(
        "1. Informations générales",
        styles["TitreSection"]
    ))

    informations = [
        [
            Paragraph("<b>Profil du poste</b>", styles["TexteCellule"]),
            Paragraph(escape(str(nom_profil)), styles["TexteCellule"])
        ],
        [
            Paragraph("<b>Date du rapport</b>", styles["TexteCellule"]),
            Paragraph(
                datetime.now().strftime("%d/%m/%Y à %H:%M"),
                styles["TexteCellule"]
            )
        ],
        [
            Paragraph("<b>Nombre de contrôles</b>", styles["TexteCellule"]),
            Paragraph(str(len(resultats)), styles["TexteCellule"])
        ]
    ]

    tableau_infos = Table(
        informations,
        colWidths=[5 * cm, 11 * cm]
    )
    tableau_infos.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), BLEU_CLAIR),
        ("BACKGROUND", (1, 0), (1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D5D8DC")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
    ]))
    elements.append(tableau_infos)

    # Calcul du résumé
    conformes = 0
    non_conformes = 0
    autres = 0

    for resultat in resultats:
        etat = str(resultat.get("etat", "")).strip().lower()

        if "non conforme" in etat or "non-conforme" in etat:
            non_conformes += 1
        elif "conforme" in etat:
            conformes += 1
        else:
            autres += 1

    elements.append(Paragraph(
        "2. Résumé des résultats",
        styles["TitreSection"]
    ))

    resume = [
        [
            Paragraph("<b>CONFORMES</b>", styles["CelluleCentre"]),
            Paragraph("<b>NON CONFORMES</b>", styles["CelluleCentre"]),
            Paragraph("<b>AUTRES</b>", styles["CelluleCentre"])
        ],
        [
            Paragraph(str(conformes), styles["CelluleCentre"]),
            Paragraph(str(non_conformes), styles["CelluleCentre"]),
            Paragraph(str(autres), styles["CelluleCentre"])
        ]
    ]

    tableau_resume = Table(
        resume,
        colWidths=[16 / 3 * cm, 16 / 3 * cm, 16 / 3 * cm],
        rowHeights=[0.8 * cm, 1.1 * cm]
    )
    tableau_resume.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), VERT),
        ("BACKGROUND", (1, 0), (1, 0), ROUGE),
        ("BACKGROUND", (2, 0), (2, 0), GRIS),
        ("BACKGROUND", (0, 1), (-1, 1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D5D8DC")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
    ]))
    elements.append(tableau_resume)

    # Verdict final
    elements.append(Paragraph(
        "3. Verdict de la recette",
        styles["TitreSection"]
    ))

    verdict_texte = str(verdict)
    verdict_couleur = (
        ROUGE if "non conforme" in verdict_texte.lower()
        else VERT if "conforme" in verdict_texte.lower()
        else BLEU_CLAIR
    )

    tableau_verdict = Table(
        [[Paragraph(escape(verdict_texte), styles["Verdict"])]],
        colWidths=[16 * cm]
    )
    tableau_verdict.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), verdict_couleur),
        ("BOX", (0, 0), (-1, -1), 1, BLEU),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12)
    ]))
    elements.append(tableau_verdict)

    # Détail de tous les contrôles
    elements.append(Paragraph(
        "4. Détail des contrôles",
        styles["TitreSection"]
    ))

    donnees = [
        [
            Paragraph("<b>N°</b>", styles["CelluleCentre"]),
            Paragraph("<b>Contrôle effectué</b>", styles["TexteCellule"]),
            Paragraph("<b>Résultat</b>", styles["CelluleCentre"])
        ]
    ]

    for numero, resultat in enumerate(resultats, start=1):
        nom_controle = escape(str(resultat.get("controle", "Non renseigné")))
        etat = escape(str(resultat.get("etat", "Non renseigné")))

        donnees.append([
            Paragraph(str(numero), styles["CelluleCentre"]),
            Paragraph(nom_controle, styles["TexteCellule"]),
            Paragraph(etat, styles["CelluleCentre"])
        ])

    tableau_controles = Table(
        donnees,
        colWidths=[1.2 * cm, 10.3 * cm, 4.5 * cm],
        repeatRows=1,
        hAlign="LEFT"
    )

    commandes_style = [
        ("BACKGROUND", (0, 0), (-1, 0), BLEU_FONCE),
        ("TEXTCOLOR", (0, 0), (-1, 0), BLANC),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D5D8DC")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7)
    ]

    for ligne, resultat in enumerate(resultats, start=1):
        etat = str(resultat.get("etat", "")).lower()

        if "non conforme" in etat or "non-conforme" in etat:
            couleur = ROUGE
        elif "conforme" in etat:
            couleur = VERT
        else:
            couleur = GRIS

        commandes_style.append(
            ("BACKGROUND", (2, ligne), (2, ligne), couleur)
        )

        if ligne % 2 == 0:
            commandes_style.append(
                ("BACKGROUND", (0, ligne), (1, ligne), GRIS)
            )

    tableau_controles.setStyle(TableStyle(commandes_style))
    elements.append(tableau_controles)

    elements.append(Spacer(1, 0.6 * cm))
    elements.append(Paragraph(
        "Rapport généré automatiquement par l'application "
        "de recette informatique.",
        styles["SousTitre"]
    ))

    # Pied de page et numéro de page
    def ajouter_pied_de_page(canvas, doc):
        canvas.saveState()
        largeur, hauteur = A4

        canvas.setStrokeColor(BLEU)
        canvas.setLineWidth(0.6)
        canvas.line(
            1.7 * cm,
            1.35 * cm,
            largeur - 1.7 * cm,
            1.35 * cm
        )

        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(GRIS_TEXTE)
        canvas.drawString(
            1.7 * cm,
            0.9 * cm,
            "Projet 1 SLAM - Rapport de recette"
        )
        canvas.drawRightString(
            largeur - 1.7 * cm,
            0.9 * cm,
            f"Page {doc.page}"
        )
        canvas.restoreState()

    document.build(
        elements,
        onFirstPage=ajouter_pied_de_page,
        onLaterPages=ajouter_pied_de_page
    )

    return nom_fichier

